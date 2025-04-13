"""
Current List of Exceptions. Can be translated.
"""
_no_unload_subclasses = True # Don't unload subclasses
from locale_str import locale_str_ex as _ # use _ as translation wrapper
from typing import *

if "CustomException" in globals(): # don't define the class again if it is being hot reloaded
    CustomException = globals()['CustomException'] # nop, just to fool linter
else:
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
    def __init__(self, category: str="card", card_name: Optional[str]=None, message: Optional[str]=None):
        suffix = ""
        if message is not None:
            suffix = "\n\n" + message
        if card_name is None:
            super().__init__("The specified {} is not found.".format(category.lower()) + suffix)
        else:
            super().__init__("The specified {} ({}) is not found.".format(category.lower(), card_name) + suffix)

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

class DataNotExistException(CustomException):
    """
    There are no such entry.
    """
    def __init__(self):
        super().__init__("There is no such entry.")

class EventNotFoundException(CustomException):
    """
    Event not found.
    """
    def __init__(self):
        super().__init__("Event not found.")

class EventNotInProgressException(CustomException):
    """
    Event not in progress.
    """
    def __init__(self):
        super().__init__("Event not in progress.")

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

class FileNotExistException(CustomException):
    """
    The requested file is not found.
    """
    def __init__(self):
        super().__init__("The requested file is not found.")

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
            from basic_utility import guild_filesize_limit
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

class InvalidArgumentException(CustomException):
    """
    Invalid argument specified.
    """
    def __init__(self, message: Optional[str]=None):
        if message is None:
            super().__init__("Invalid argument specified.")
        else:
            super().__init__("Invalid argument specified.\n\n" + message)

class InvalidPlayerIDException(CustomException):
    """
    Invalid Player ID specified.
    """
    def __init__(self, category: str="player"):
        super().__init__(f"Invalid {category.title()} ID specified.")

class InvalidPayloadException(CustomException):
    def __init__(self, lines: List[str]):
        super().__init__("\n".join(lines))

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

class RankNotFoundException(CustomException):
    """
    The specified rank is not found.
    """
    def __init__(self):
        super().__init__("The specified rank is not found.")

class ReadonlyUserException(CustomException):
    """
    Other users can only perform read-only operations.
    """
    def __init__(self):
        super().__init__("Other users can only perform read-only operations.")

class RoomNotFoundException(CustomException):
    """
    The specified room is not found.
    """
    def __init__(self):
        super().__init__("The specified room is not found.")

class SongDifficultyNotFoundException(CustomException):
    """
    The difficulty is not found for the song.
    """
    def __init__(self, difficulty: Optional[str] = None, song_name: Optional[str] = None):
        difficulty_text = "" if difficulty is None else f" ({difficulty})"
        song_name_text = "" if song_name is None else f" ({song_name})"
        super().__init__(f"The difficulty{difficulty_text} is not found for the song{song_name_text}.")

class SongNotFoundException(CustomException):
    """
    Song not found.
    """
    def __init__(self, suggestions: Optional[List[str]] = None):
        if suggestions is None:
            super().__init__("Song not found.")
        else:
            char_count = 0
            all_suggestions = []
            for entry in suggestions:
                if char_count + len(entry) > 2000:
                    break
                all_suggestions.append(entry)
                char_count += len(entry) + 1
            super().__init__("Song not found. Do you mean ...\n\n" + "\n".join(all_suggestions))

class SongTrackNotFoundException(CustomException):
    """
    Song Track not found.
    """
    def __init__(self):
        super().__init__("Song Track not found.")

class StampNotFoundException(CustomException):
    """
    Stamp not found.
    """
    def __init__(self):
        super().__init__("Stamp not found.")

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
        super().__init__("Unreleased Contents are Hidden in this Channel.\n(Consider using the command without the trailing '_' in the game name if the bot is installed in a server.)")

class UserNotFoundException(CustomException):
    """
    The specified user is not found.
    """
    def __init__(self):
        super().__init__("The specified user is not found.")

class VersionHashNotFoundException(CustomException):
    """
    The hash for the current version is not found.
    """
    def __init__(self):
        super().__init__("The hash for the current version is not found.")

class WorkInProgressException(CustomException):
    """
    This feature is being developed in progress.
    """
    def __init__(self):
        super().__init__("This feature is being developed in progress.")