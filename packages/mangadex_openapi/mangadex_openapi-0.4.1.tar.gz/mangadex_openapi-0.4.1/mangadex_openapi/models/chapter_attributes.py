# coding: utf-8

"""
    MangaDex API

    MangaDex is an ad-free manga reader offering high-quality images!  This document details our API as it is right now. It is in no way a promise to never change it, although we will endeavour to publicly notify any major change.  # Authentication  You can login with the `/auth/login` endpoint. On success, it will return a JWT that remains valid for 15 minutes along with a session token that allows refreshing without re-authenticating for 1 month.  # Rate limits  The API enforces rate-limits to protect our servers against malicious and/or mistaken use. The API keeps track of the requests on an IP-by-IP basis. Hence, if you're on a VPN, proxy or a shared network in general, the requests of other users on this network might affect you.  At first, a **global limit of 5 requests per second per IP address** is in effect.  > This limit is enforced across multiple load-balancers, and thus is not an exact value but rather a lower-bound that we guarantee. The exact value will be somewhere in the range `[5, 5*n]` (with `n` being the number of load-balancers currently active). The exact value within this range will depend on the current traffic patterns we are experiencing.  On top of this, **some endpoints are further restricted** as follows:  | Endpoint                           | Requests per time period    | Time period in minutes | |------------------------------------|--------------------------   |------------------------| | `POST   /account/create`           | 1                           | 60                     | | `GET    /account/activate/{code}`  | 30                          | 60                     | | `POST   /account/activate/resend`  | 5                           | 60                     | | `POST   /account/recover`          | 5                           | 60                     | | `POST   /account/recover/{code}`   | 5                           | 60                     | | `POST   /auth/login`               | 30                          | 60                     | | `POST   /auth/refresh`             | 30                          | 60                     | | `POST   /author`                   | 10                          | 60                     | | `PUT    /author`                   | 10                          | 1                      | | `DELETE /author/{id}`              | 10                          | 10                     | | `POST   /captcha/solve`            | 10                          | 10                     | | `POST   /chapter/{id}/read`        | 300                         | 10                     | | `PUT    /chapter/{id}`             | 10                          | 1                      | | `DELETE /chapter/{id}`             | 10                          | 1                      | | `POST   /manga`                    | 10                          | 60                     | | `PUT    /manga/{id}`               | 10                          | 60                     | | `DELETE /manga/{id}`               | 10                          | 10                     | | `POST   /cover`                    | 10                          | 1                      | | `PUT    /cover/{id}`               | 10                          | 1                      | | `DELETE /cover/{id}`               | 10                          | 10                     | | `POST   /group`                    | 10                          | 60                     | | `PUT    /group/{id}`               | 10                          | 1                      | | `DELETE /group/{id}`               | 10                          | 10                     | | `GET    /at-home/server/{id}`      | 60                          | 1                      |  Calling these endpoints will further provide details via the following headers about your remaining quotas:  | Header                    | Description                                                                 | |---------------------------|-----------------------------------------------------------------------------| | `X-RateLimit-Limit`       | Maximal number of requests this endpoint allows per its time period         | | `X-RateLimit-Remaining`   | Remaining number of requests within your quota for the current time period  | | `X-RateLimit-Retry-After` | Timestamp of the end of the current time period, as UNIX timestamp          |  # Captchas  Some endpoints may require captchas to proceed, in order to slow down automated malicious traffic. Legitimate users might also be affected, based on the frequency of write requests or due certain endpoints being particularly sensitive to malicious use, such as user signup.  Once an endpoint decides that a captcha needs to be solved, a 403 Forbidden response will be returned, with the error code `captcha_required_exception`. The sitekey needed for recaptcha to function is provided in both the `X-Captcha-Sitekey` header field, as well as in the error context, specified as `siteKey` parameter.  The captcha result of the client can either be passed into the repeated original request with the `X-Captcha-Result` header or alternatively to the `POST /captcha/solve` endpoint. The time a solved captcha is remembered varies across different endpoints and can also be influenced by individual client behavior.  Authentication is not required for the `POST /captcha/solve` endpoint, captchas are tracked both by client ip and logged in user id. If you are logged in, you want to send the session token along, so you validate the captcha for your client ip and user id at the same time, but it is not required.  # Reading a chapter using the API  ## Retrieving pages from the MangaDex@Home network  A valid [MangaDex@Home network](https://mangadex.network) page URL is in the following format: `{server-specific base url}/{temporary access token}/{quality mode}/{chapter hash}/{filename}`  There are currently 2 quality modes: - `data`: Original upload quality - `data-saver`: Compressed quality  Upon fetching a chapter from the API, you will find 4 fields necessary to compute MangaDex@Home page URLs:  | Field                        | Type     | Description                       | |------------------------------|----------|-----------------------------------| | `.data.id`                   | `string` | API Chapter ID                    | | `.data.attributes.hash`      | `string` | MangaDex@Home Chapter Hash        | | `.data.attributes.data`      | `array`  | data quality mode filenames       | | `.data.attributes.dataSaver` | `array`  | data-saver quality mode filenames |  Example ```json GET /chapter/{id}  {   ...,   \"data\": {     \"id\": \"e46e5118-80ce-4382-a506-f61a24865166\",     ...,     \"attributes\": {       ...,       \"hash\": \"e199c7d73af7a58e8a4d0263f03db660\",       \"data\": [         \"x1-b765e86d5ecbc932cf3f517a8604f6ac6d8a7f379b0277a117dc7c09c53d041e.png\",         ...       ],       \"dataSaver\": [         \"x1-ab2b7c8f30c843aa3a53c29bc8c0e204fba4ab3e75985d761921eb6a52ff6159.jpg\",         ...       ]     }   } } ```  From this point you miss only the base URL to an assigned MangaDex@Home server for your client and chapter. This is retrieved via a `GET` request to `/at-home/server/{ chapter .data.id }`.  Example: ```json GET /at-home/server/e46e5118-80ce-4382-a506-f61a24865166  {   \"baseUrl\": \"https://abcdefg.hijklmn.mangadex.network:12345/some-token\" } ```  The full URL is the constructed as follows ``` { server .baseUrl }/{ quality mode }/{ chapter .data.attributes.hash }/{ chapter .data.attributes.{ quality mode }.[*] }  Examples  data quality: https://abcdefg.hijklmn.mangadex.network:12345/some-token/data/e199c7d73af7a58e8a4d0263f03db660/x1-b765e86d5ecbc932cf3f517a8604f6ac6d8a7f379b0277a117dc7c09c53d041e.png        base url: https://abcdefg.hijklmn.mangadex.network:12345/some-token   quality mode: data   chapter hash: e199c7d73af7a58e8a4d0263f03db660       filename: x1-b765e86d5ecbc932cf3f517a8604f6ac6d8a7f379b0277a117dc7c09c53d041e.png   data-saver quality: https://abcdefg.hijklmn.mangadex.network:12345/some-token/data-saver/e199c7d73af7a58e8a4d0263f03db660/x1-ab2b7c8f30c843aa3a53c29bc8c0e204fba4ab3e75985d761921eb6a52ff6159.jpg        base url: https://abcdefg.hijklmn.mangadex.network:12345/some-token   quality mode: data-saver   chapter hash: e199c7d73af7a58e8a4d0263f03db660       filename: x1-ab2b7c8f30c843aa3a53c29bc8c0e204fba4ab3e75985d761921eb6a52ff6159.jpg ```  If the server you have been assigned fails to serve images, you are allowed to call the `/at-home/server/{ chapter id }` endpoint again to get another server.  Whether successful or not, **please do report the result you encountered as detailed below**. This is so we can pull the faulty server out of the network.  ## Report  In order to keep track of the health of the servers in the network and to improve the quality of service and reliability, we ask that you call the MangaDex@Home report endpoint after each image you retrieve, whether successfully or not.  It is a `POST` request against `https://api.mangadex.network/report` and expects the following payload with our example above:  | Field                       | Type       | Description                                                                         | |-----------------------------|------------|-------------------------------------------------------------------------------------| | `url`                       | `string`   | The full URL of the image                                                           | | `success`                   | `boolean`  | Whether the image was successfully retrieved                                        | | `cached `                   | `boolean`  | `true` iff the server returned an `X-Cache` header with a value starting with `HIT` | | `bytes`                     | `number`   | The size in bytes of the retrieved image                                            | | `duration`                  | `number`   | The time in miliseconds that the complete retrieval (not TTFB) of this image took   |  Examples herafter.  **Success:** ```json POST https://api.mangadex.network/report Content-Type: application/json  {   \"url\": \"https://abcdefg.hijklmn.mangadex.network:12345/some-token/data/e199c7d73af7a58e8a4d0263f03db660/x1-b765e86d5ecbc932cf3f517a8604f6ac6d8a7f379b0277a117dc7c09c53d041e.png\",   \"success\": true,   \"bytes\": 727040,   \"duration\": 235,   \"cached\": true } ```  **Failure:** ```json POST https://api.mangadex.network/report Content-Type: application/json  {  \"url\": \"https://abcdefg.hijklmn.mangadex.network:12345/some-token/data/e199c7d73af7a58e8a4d0263f03db660/x1-b765e86d5ecbc932cf3f517a8604f6ac6d8a7f379b0277a117dc7c09c53d041e.png\",  \"success\": false,  \"bytes\": 25,  \"duration\": 235,  \"cached\": false } ```  While not strictly necessary, this helps us monitor the network's healthiness, and we appreciate your cooperation towards this goal. If no one reports successes and failures, we have no way to know that a given server is slow/broken, which eventually results in broken image retrieval for everyone.  # Retrieving Covers from the API  ## Construct Cover URLs  ### Source (original/best quality)  `https://uploads.mangadex.org/covers/{ manga.id }/{ cover.filename }`<br/> The extension can be png, jpeg or gif.  Example: `https://uploads.mangadex.org/covers/8f3e1818-a015-491d-bd81-3addc4d7d56a/4113e972-d228-4172-a885-cb30baffff97.jpg`  ### <=512px wide thumbnail  `https://uploads.mangadex.org/covers/{ manga.id }/{ cover.filename }.512.jpg`<br/> The extension is always jpg.  Example: `https://uploads.mangadex.org/covers/8f3e1818-a015-491d-bd81-3addc4d7d56a/4113e972-d228-4172-a885-cb30baffff97.jpg.512.jpg`  ### <=256px wide thumbnail  `https://uploads.mangadex.org/covers/{ manga.id }/{ cover.filename }.256.jpg`<br/> The extension is always jpg.  Example: `https://uploads.mangadex.org/covers/8f3e1818-a015-491d-bd81-3addc4d7d56a/4113e972-d228-4172-a885-cb30baffff97.jpg.256.jpg`  ## ℹ️ Where to find Cover filename ?  Look at the [Get cover operation](#operation/get-cover) endpoint to get Cover information. Also, if you get a Manga resource, you'll have, if available a `covert_art` relationship which is the main cover id.  # Static data  ## Manga publication demographic  | Value            | Description               | |------------------|---------------------------| | shounen          | Manga is a Shounen        | | shoujo           | Manga is a Shoujo         | | josei            | Manga is a Josei          | | seinen           | Manga is a Seinen         |  ## Manga status  | Value            | Description               | |------------------|---------------------------| | ongoing          | Manga is still going on   | | completed        | Manga is completed        | | hiatus           | Manga is paused           | | cancelled        | Manga has been cancelled  |  ## Manga reading status  | Value            | |------------------| | reading          | | on_hold          | | plan\\_to\\_read   | | dropped          | | re\\_reading      | | completed        |  ## Manga content rating  | Value            | Description               | |------------------|---------------------------| | safe             | Safe content              | | suggestive       | Suggestive content        | | erotica          | Erotica content           | | pornographic     | Pornographic content      |  ## CustomList visibility  | Value            | Description               | |------------------|---------------------------| | public           | CustomList is public      | | private          | CustomList is private     |  ## Relationship types  | Value            | Description                    | |------------------|--------------------------------| | manga            | Manga resource                 | | chapter          | Chapter resource               | | cover_art        | A Cover Art for a manga `*`    | | author           | Author resource                | | artist           | Author resource (drawers only) | | scanlation_group | ScanlationGroup resource       | | tag              | Tag resource                   | | user             | User resource                  | | custom_list      | CustomList resource            |  `*` Note, that on manga resources you get only one cover_art resource relation marking the primary cover if there are more than one. By default this will be the latest volume's cover art. If you like to see all the covers for a given manga, use the cover search endpoint for your mangaId and select the one you wish to display.  ## Manga links data  In Manga attributes you have the `links` field that is a JSON object with some strange keys, here is how to decode this object:  | Key   | Related site  | URL                                                                                           | URL details                                                    | |-------|---------------|-----------------------------------------------------------------------------------------------|----------------------------------------------------------------| | al    | anilist       | https://anilist.co/manga/`{id}`                                                               | Stored as id                                                   | | ap    | animeplanet   | https://www.anime-planet.com/manga/`{slug}`                                                   | Stored as slug                                                 | | bw    | bookwalker.jp | https://bookwalker.jp/`{slug}`                                                                | Stored has \"series/{id}\"                                       | | mu    | mangaupdates  | https://www.mangaupdates.com/series.html?id=`{id}`                                            | Stored has id                                                  | | nu    | novelupdates  | https://www.novelupdates.com/series/`{slug}`                                                  | Stored has slug                                                | | kt    | kitsu.io      | https://kitsu.io/api/edge/manga/`{id}` or https://kitsu.io/api/edge/manga?filter[slug]={slug} | If integer, use id version of the URL, otherwise use slug one  | | amz   | amazon        | N/A                                                                                           | Stored as full URL                                             | | ebj   | ebookjapan    | N/A                                                                                           | Stored as full URL                                             | | mal   | myanimelist   | https://myanimelist.net/manga/{id}                                                            | Store as id                                                    | | raw   | N/A           | N/A                                                                                           | Stored as full URL, untranslated stuff URL (original language) | | engtl | N/A           | N/A                                                                                           | Stored as full URL, official english licenced URL              |  # noqa: E501

    OpenAPI spec version: 5.0.21
    Contact: mangadexstaff@gmail.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six


class ChapterAttributes(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        "title": "str",
        "volume": "str",
        "chapter": "str",
        "translated_language": "str",
        "hash": "str",
        "data": "list[str]",
        "data_saver": "list[str]",
        "uploader": "str",
        "version": "int",
        "created_at": "str",
        "updated_at": "str",
        "publish_at": "str",
    }

    attribute_map = {
        "title": "title",
        "volume": "volume",
        "chapter": "chapter",
        "translated_language": "translatedLanguage",
        "hash": "hash",
        "data": "data",
        "data_saver": "dataSaver",
        "uploader": "uploader",
        "version": "version",
        "created_at": "createdAt",
        "updated_at": "updatedAt",
        "publish_at": "publishAt",
    }

    def __init__(
        self,
        title=None,
        volume=None,
        chapter=None,
        translated_language=None,
        hash=None,
        data=None,
        data_saver=None,
        uploader=None,
        version=None,
        created_at=None,
        updated_at=None,
        publish_at=None,
    ):  # noqa: E501
        """ChapterAttributes - a model defined in Swagger"""  # noqa: E501
        self._title = None
        self._volume = None
        self._chapter = None
        self._translated_language = None
        self._hash = None
        self._data = None
        self._data_saver = None
        self._uploader = None
        self._version = None
        self._created_at = None
        self._updated_at = None
        self._publish_at = None
        self.discriminator = None
        if title is not None:
            self.title = title
        if volume is not None:
            self.volume = volume
        if chapter is not None:
            self.chapter = chapter
        if translated_language is not None:
            self.translated_language = translated_language
        if hash is not None:
            self.hash = hash
        if data is not None:
            self.data = data
        if data_saver is not None:
            self.data_saver = data_saver
        if uploader is not None:
            self.uploader = uploader
        if version is not None:
            self.version = version
        if created_at is not None:
            self.created_at = created_at
        if updated_at is not None:
            self.updated_at = updated_at
        if publish_at is not None:
            self.publish_at = publish_at

    @property
    def title(self):
        """Gets the title of this ChapterAttributes.  # noqa: E501


        :return: The title of this ChapterAttributes.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this ChapterAttributes.


        :param title: The title of this ChapterAttributes.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def volume(self):
        """Gets the volume of this ChapterAttributes.  # noqa: E501


        :return: The volume of this ChapterAttributes.  # noqa: E501
        :rtype: str
        """
        return self._volume

    @volume.setter
    def volume(self, volume):
        """Sets the volume of this ChapterAttributes.


        :param volume: The volume of this ChapterAttributes.  # noqa: E501
        :type: str
        """

        self._volume = volume

    @property
    def chapter(self):
        """Gets the chapter of this ChapterAttributes.  # noqa: E501


        :return: The chapter of this ChapterAttributes.  # noqa: E501
        :rtype: str
        """
        return self._chapter

    @chapter.setter
    def chapter(self, chapter):
        """Sets the chapter of this ChapterAttributes.


        :param chapter: The chapter of this ChapterAttributes.  # noqa: E501
        :type: str
        """

        self._chapter = chapter

    @property
    def translated_language(self):
        """Gets the translated_language of this ChapterAttributes.  # noqa: E501


        :return: The translated_language of this ChapterAttributes.  # noqa: E501
        :rtype: str
        """
        return self._translated_language

    @translated_language.setter
    def translated_language(self, translated_language):
        """Sets the translated_language of this ChapterAttributes.


        :param translated_language: The translated_language of this ChapterAttributes.  # noqa: E501
        :type: str
        """

        self._translated_language = translated_language

    @property
    def hash(self):
        """Gets the hash of this ChapterAttributes.  # noqa: E501


        :return: The hash of this ChapterAttributes.  # noqa: E501
        :rtype: str
        """
        return self._hash

    @hash.setter
    def hash(self, hash):
        """Sets the hash of this ChapterAttributes.


        :param hash: The hash of this ChapterAttributes.  # noqa: E501
        :type: str
        """

        self._hash = hash

    @property
    def data(self):
        """Gets the data of this ChapterAttributes.  # noqa: E501


        :return: The data of this ChapterAttributes.  # noqa: E501
        :rtype: list[str]
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this ChapterAttributes.


        :param data: The data of this ChapterAttributes.  # noqa: E501
        :type: list[str]
        """

        self._data = data

    @property
    def data_saver(self):
        """Gets the data_saver of this ChapterAttributes.  # noqa: E501


        :return: The data_saver of this ChapterAttributes.  # noqa: E501
        :rtype: list[str]
        """
        return self._data_saver

    @data_saver.setter
    def data_saver(self, data_saver):
        """Sets the data_saver of this ChapterAttributes.


        :param data_saver: The data_saver of this ChapterAttributes.  # noqa: E501
        :type: list[str]
        """

        self._data_saver = data_saver

    @property
    def uploader(self):
        """Gets the uploader of this ChapterAttributes.  # noqa: E501


        :return: The uploader of this ChapterAttributes.  # noqa: E501
        :rtype: str
        """
        return self._uploader

    @uploader.setter
    def uploader(self, uploader):
        """Sets the uploader of this ChapterAttributes.


        :param uploader: The uploader of this ChapterAttributes.  # noqa: E501
        :type: str
        """

        self._uploader = uploader

    @property
    def version(self):
        """Gets the version of this ChapterAttributes.  # noqa: E501


        :return: The version of this ChapterAttributes.  # noqa: E501
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this ChapterAttributes.


        :param version: The version of this ChapterAttributes.  # noqa: E501
        :type: int
        """

        self._version = version

    @property
    def created_at(self):
        """Gets the created_at of this ChapterAttributes.  # noqa: E501


        :return: The created_at of this ChapterAttributes.  # noqa: E501
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this ChapterAttributes.


        :param created_at: The created_at of this ChapterAttributes.  # noqa: E501
        :type: str
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this ChapterAttributes.  # noqa: E501


        :return: The updated_at of this ChapterAttributes.  # noqa: E501
        :rtype: str
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this ChapterAttributes.


        :param updated_at: The updated_at of this ChapterAttributes.  # noqa: E501
        :type: str
        """

        self._updated_at = updated_at

    @property
    def publish_at(self):
        """Gets the publish_at of this ChapterAttributes.  # noqa: E501


        :return: The publish_at of this ChapterAttributes.  # noqa: E501
        :rtype: str
        """
        return self._publish_at

    @publish_at.setter
    def publish_at(self, publish_at):
        """Sets the publish_at of this ChapterAttributes.


        :param publish_at: The publish_at of this ChapterAttributes.  # noqa: E501
        :type: str
        """

        self._publish_at = publish_at

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value
        if issubclass(ChapterAttributes, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ChapterAttributes):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
