class CustomException(Exception):
    pass

class APIFailException(CustomException):
    """
    API call fails. Please try again later.
    """
    def __init__(self, message=None, code=None):
        self.code = code
        if message is None:
            if code is not None:
                super().__init__("API call fails. Please try again later. (Code: {})".format(code))
            else:
                super().__init__("API call fails. Please try again later.")
        else:
            if code is not None:
                super().__init__("{} (Code: {})".format(message, code))
            else:
                super().__init__(message)

class AssetDownloadException(CustomException):
    """
    The specified asset cannot be downloaded.
    """
    def __init__(self):
        super().__init__("The specified asset cannot be downloaded.")

class AssetListDownloadException(CustomException):
    """
    Asset List for the current version cannot be downloaded.
    """
    def __init__(self):
        super().__init__("Asset List for the current version cannot be downloaded.")

class AssetListNotExistException(CustomException):
    """
    Asset List is not Available.
    """
    def __init__(self):
        super().__init__("Asset List is not Available.")

class AssetNotExistException(CustomException):
    """
    The specified asset does not exist.
    """
    def __init__(self):
        super().__init__("The specified asset does not exist.")

class CardNotFoundException(CustomException):
    """
    The specified card is not found.
    """
    def __init__(self, category="card", card_name=None):
        if card_name is None:
            super().__init__("The specified {} is not found.".format(category.lower()))
        else:
            super().__init__("The specified {} ({}) is not found.".format(category.lower(), card_name))

class CircleNotFoundException(CustomException):
    """
    The specified circle is not found.
    """
    def __init__(self):
        super().__init__("The specified circle is not found.")

class CharacterNotFoundException(CustomException):
    """
    The specified character is not found.
    """
    def __init__(self):
        super().__init__("The specified character is not found.")

class DataUnavailableException(CustomException):
    """
    The requested data is not available.
    """
    def __init__(self):
        super().__init__("The requested data is not available.")

class EventNotFoundException(CustomException):
    """
    Event not found.
    """
    def __init__(self):
        super().__init__("Event not found.")

class EventRankingModeNotExistException(CustomException):
    """
    This ranking mode is not available for this event.
    """
    def __init__(self):
        super().__init__("This ranking mode is not available for this event.")

class FileEncryptedException(CustomException):
    """
    The requested file is encrypted and the decrypt method is unknown.
    """
    def __init__(self):
        super().__init__("The requested file is encrypted and the decrypt method is unknown.")

class FileSizeExceededException(CustomException):
    """
    The requested file is too large to be sent to this server.
    """
    def __init__(self, guild=..., count=..., filename=...):
        if count is ...:
            if filename is ...:
                msg = "The requested file is too large to be sent to this server."
            else:
                msg = "The requested file ({}) is too large to be sent to this server.".format(filename)
        else:
            msg = "{} of the requested file(s) {} too large to be sent to this server.".format(count, "are" if count > 1 else "is")
        if guild is not ...:
            from discord_utility import guild_filesize_limit
            msg += " Maximum file size: {} MB".format(guild_filesize_limit(guild) >> 20)
        super().__init__(msg)

class FormatException(CustomException):
    """
    The provided string does not match the format.
    """
    def __init__(self):
        super().__init__("The provided string does not match the format.")

class HTTPException(CustomException):
    """
    Error fetching data. Response code: ...
    """
    def __init__(self, response_code):
        super().__init__("Error fetching data. Response code: {}".format(response_code))

class MasterDatabaseDownloadException(CustomException):
    """
    Master Database for the current version cannot be downloaded.
    """
    def __init__(self):
        super().__init__("Master Database for the current version cannot be downloaded.")

class PayloadTooLargeException(CustomException):
    """
    The provided payload is too large to be sent.
    """
    def __init__(self, max_char=...):
        if max_char is ...:
            super().__init__("The provided payload is too large to be sent.")
        else:
            super().__init__("The provided payload is too large to be sent. (Max: {} Characters)".format(max_char))

class PermissionDeniedException(CustomException):
    """
    Permission Denied. Required Permission: {}
    """
    def __init__(self, perm=None):
        if perm is None:
            super().__init__("Permission Denied.")
        else:
            super().__init__("Permission Denied. Required Permission: {}".format(perm))

class PlayerNotFoundException(CustomException):
    """
    The specified player is not found.
    """
    def __init__(self):
        super().__init__("The specified player is not found.")

class RankNotFoundException(CustomException):
    """
    The specified rank is not found.
    """
    def __init__(self):
        super().__init__("The specified rank is not found.")

class SongDifficultyNotFoundException(CustomException):
    """
    The difficulty is not found for the song.
    """
    def __init__(self):
        super().__init__("The difficulty is not found for the song.")

class SongNotFoundException(CustomException):
    """
    Song not found.
    """
    def __init__(self):
        super().__init__("Song not found.")

class TableNotFoundException(CustomException):
    """
    The specified table is not found.
    """
    def __init__(self):
        super().__init__("The specified table is not found.")

class TimeFormatException(CustomException):
    """
    The time format is not recognized.
    """
    def __init__(self):
        super().__init__("The time format is not recognized.")

class UnmatchedExtensionException(CustomException):
    """
    The specified file does not match the expected extension.
    """
    def __init__(self, ext=None):
        if ext is None:
            super().__init__("The specified file does not match the expected extension.")
        elif isinstance(ext, list) or isinstance(ext, tuple):
            super().__init__("The specified file does not match the expected extension.\nExpected Extension: {}".format(",".join(ext)))
        else:
            super().__init__("The specified file does not match the expected extension.\nExpected Extension: {}".format(ext))

class UnreleasedContentException(CustomException):
    """
    Unreleased Contents are Hidden in this Channel.
    """
    def __init__(self):
        super().__init__("Unreleased Contents are Hidden in this Channel.")

class WorkInProgressException(CustomException):
    """
    This feature is being developed in progress.
    """
    def __init__(self):
        super().__init__("This feature is being developed in progress.")