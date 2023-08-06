# coding: utf8
"""Classes here wrap parts of the mangadex API for more version-agonistic code.

Almost every API class from mangadex_openapi has a corrosponding mixin
(i.e MangaApi -> MangaMixin).
This keeps the glue code contained within their own classes.

But you can just import the `QuickClient` class which subclasses all mixins:

```python
from mangadex_openapi import QuickClient
```

and then initalise it:

```python
client = QuickClient()
```

Finally, use it.

```python
manga = client.manga_("a96676e5-8ae2-425e-b549-7f15dd34a6d8")
```
"""

import logging
from typing import List, Literal, Optional

import mangadex_openapi as mangadex

from . import utils

_log = logging.getLogger("mangadex")


class Client:
    """Base client that wraps mangadex.ApiClient.

    Attributes:
        session_token (str): The token for the current session.
        persist_token (str): The token for the persistent session (can be reused later on).
    """

    def __init__(self):
        self.client = mangadex.ApiClient()

        self._apis = {}
        self.session_token = None
        self.persist_token = None

    def __getattr__(self, attr):
        # i.e accessing self.manga will initalize MangaApi and save it in self._apis
        if attr not in self._apis:
            self._apis[attr] = getattr(mangadex, f"{utils.camel_case(attr)}Api")(
                self.client
            )

        return self._apis[attr]

    def ping(self) -> bool:
        """Ping the Mangadex server to check whether it is online."""

        return self.infrastructure.ping_get() == "pong"


class AccountMixin:
    def create_account(self, **kwargs):
        """Create a Mangadex account.

        Note that you have to activate the account before you can use it.
        Check the email's inbox for an actvation code, and then run client.activate_account("activation code").

        Args:
            username (str): The new account name.
            password (str): The new account password.
            email (str): The email to register the new account to.
        """

        self.account.post_account_create(body=mangadex.CreateAccount(**kwargs))

    def activate_account(self, code: str):
        """Activate a Mangadex account using a code sent to its email.

        Args:
            code: The activation code.
        """

        self.account.get_account_activate_code(code)

    def actiavte_resend(self, email: str):
        """Resend an activation code to a new Mangadex account.

        Args:
            email: The new account's email.
        """

        body = mangadex.SendAccountActivationCode(email=email)
        self.account.post_account_activate_resend(body=body)

    def recover_account(self, email: str):
        """Recover a Mangadex account
        (i.e if you forgot your password).

        A recovery code is sent to the email of the account, so call client.recover_complete("code", "new password").

        Args:
            email: The account's email.
        """

        body = mangadex.SendAccountActivationCode(email=email)
        self.account.post_account_recover(body=body)

    def recover_complete(self, code: str, password: str):
        """Complete recovery of a Mangadex account.

        Args:
            code: The recovery code sent to the account's email.
            password: The new password to change the account to.
        """

        body = mangadex.RecoverCompleteBody(new_password=password)
        self.account.post_account_recover_code(code, body=body)


class AuthMixin:
    def login(self, username: str, password: str):
        """Authenticate this client by logging in.

        Args:
            username: The account name.
            password: The account password.
        """

        resp = self.auth.post_auth_login(
            mangadex.Login(username=username, password=password)
        )

        self._refresh(resp)

    def logout(self):
        """Deauthenticate this client by logging out."""
        self.auth.post_auth_logout()

        del self.client.default_headers["Authorization"]

    def refresh(self):
        """Refresh this client's session token (expires every 15 minutes)."""
        body = mangadex.RefreshToken(token=self.persist_token)
        resp = self.auth.post_auth_refresh(body=body)

        _log.debug("refresh message: %s", resp.message)

        self._refresh(resp)

    def check(self) -> mangadex.CheckResponse:
        """Get the authentication status of this client."""

        return self.auth.get_auth_check()

    def _refresh(self, resp):
        self.session_token = resp.token.session
        self.persist_token = resp.token.refresh

        self.client.default_headers["Authorization"] = f"Bearer {self.session_token}"


class AtHomeMixin:
    def server(self, **kwargs) -> str:
        """Get the server url for a chapter id.

        Args:
            chapter_id: The UUID of the chapter.
            force_port443: Whether or not to only select servers using port 443 (HTTPS).
                Some networks may block connections to other ports (which Mangadex@Home servers may use).
                Defaults to False.
        """

        resp = self.at_home.get_at_home_server_chapter_id(**kwargs)
        return resp.base_url


class AuthorMixin:
    def author_(self, id: str) -> mangadex.AuthorResponse:
        """Get an author by id."""

        return self.author.get_author_id(id)

    # def create_author(self, name: str) -> mangadex.AuthorResponse:
    # """Create an author."""

    # body = mangadex.AuthorCreate(name=name)
    # return self.author.post_author(body=body)

    # def update_author(self, id: str, name: str):
    # """Change the name of author by id."""

    # body = mangadex.AuthorEdit(name=name)
    # self.author.put_author_id(id, body=body)

    # def delete_author(self, id: str):
    # """Delete the author by id."""

    # self.author.delete_author_id(id)


class ChapterMixin:
    """To use this mixin, you must subclass AtHomeMixin too."""

    def chapter_(self, id: str) -> mangadex.ChapterResponse:
        """Get a chapter by id."""

        return self.chapter.get_chapter_id(id)

    def mark_read(self, id: str):
        """Mark a chapter by id as read for the current user."""

        self.chapter.chapter_id_read(id)

    def mark_unread(self, id: str):
        """Mark a chapter by id as unread for the current user."""

        self.chapter.chapter_id_unread(id)

    def pages(
        self, chapter: mangadex.ChapterResponse, saver: bool = False
    ) -> List[str]:
        """Retreive the page urls for a given chapter.

        Args:
            chapter: The chapter response.
            saver: Whether or not to use data saver urls (lower quality but smaller download size).
                Defaults to False.

        Returns:
            A list of page urls.
        """
        attrs = chapter.data.attributes

        base_url = self.at_home.get_at_home_server_chapter_id(chapter.data.id).base_url

        if saver:
            mode = "data_saver"
            urls = attrs.data_saver
        else:
            mode = "data"
            urls = attrs.data

        return ["/".join([base_url, mode, attrs.hash, url]) for url in urls]


class MangaMixin:
    def cover_(self, id: str) -> mangadex.CoverResponse:
        """Get cover by id."""

        return self.cover.get_cover_id(id)

    def manga_(self, id: str) -> mangadex.MangaResponse:
        """Get manga by id."""

        return self.manga.get_manga_id(id)

    def aggregate(self, id: str) -> mangadex.InlineResponse200:
        """Get a summary of volume and chapter info on manga by id."""

        return self.manga.manga_id_aggregate_get(id)

    def authors(self, manga: mangadex.MangaResponse) -> List[str]:
        """Retreive the author names for a manga.

        Args:
            manga: The manga response object.

        Returns:
            A list of author names.
        """

        author_ids = utils.rselect("author", manga.relationships)
        authors = self.search.get_author(ids=author_ids)

        return [a.data.attributes.name for a in authors.results]

    def chapters(self, id: str, **criteria) -> mangadex.ChapterList:
        """Get chapters for a manga by id."""

        utils.convert_datetime(criteria)

        return self.manga.get_manga_id_feed(id, **criteria)

    def cover_page(
        self, manga: mangadex.MangaResponse, *, size: Literal["og", "512", "256"] = "og"
    ) -> Optional[str]:
        """Retreive the cover url for a manga.

        Args:
            manga: The manga response object.
            size: Which cover size the url should resolve to.
                It should be one of the following (as a str):

                - `og`: Original size.
                - `512`: Thumbnail at most 512px wide.
                - `256`: Thumbnail at most 256px wide.

                Defaults to `og`.

        Returns:
            The cover url if the manga has a cover, otherwise None.
        """

        cover_id = None

        for relation in manga.relationships:
            if relation.type == "cover_art":
                cover_id = relation.id

        if cover_id is None:
            return

        cover_resp = self.cover_(cover_id)
        cover_filename = cover_resp.data.attributes.file_name

        if size == "og":
            ext = ""
        else:
            ext = f".{size}.jpg"

        return (
            f"https://uploads.mangadex.org/covers/{manga.data.id}/{cover_filename}{ext}"
        )

    def random(self) -> mangadex.MangaResponse:
        """Get a random manga.

        Returns:
            The manga response.
        """

        return self.manga.get_manga_random()


class SearchMixin:
    def search_authors(self, **criteria) -> mangadex.AuthorList:
        """Search authors by criteria."""

        return self.search.get_author(**criteria)

    def search_chapters(self, **criteria) -> mangadex.ChapterList:
        """Search chapters by criteria."""
        utils.convert_datetime(criteria)

        return self.search.get_chapter(**criteria)

    def search_covers(self, **criteria) -> mangadex.CoverList:
        """Search covers by criteria."""

        return self.search.get_cover(**criteria)

    def search_groups(self, **criteria) -> mangadex.ScanlationGroupList:
        """Search scanlation groups by criteria."""

        return self.search.get_search_group(**criteria)

    def search_manga(self, **criteria) -> mangadex.MangaList:
        """Search manga by criteria."""
        utils.convert_datetime(criteria)

        return self.search.get_search_manga(**criteria)


class QuickClient(
    AccountMixin,
    AuthMixin,
    AtHomeMixin,
    AuthorMixin,
    ChapterMixin,
    MangaMixin,
    SearchMixin,
    Client,
):
    """'Public' interface to all mixins."""

    pass
