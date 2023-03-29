import typing
import asyncio
MAX_MESSAGE_LENGTH = 3000


async def safe_split_text(text: str, length: int = MAX_MESSAGE_LENGTH, split_separator: str = ' ') -> typing.List[str]:
    """
    Split long text

    :param text:
    :param length:
    :param split_separator
    :return:
    """
    temp_text = text
    parts = []
    while temp_text:
        if len(temp_text) > length:
            try:
                split_pos = temp_text[:length].rindex(split_separator)
            except ValueError:
                split_pos = length
            if split_pos < length // 4 * 3:
                split_pos = length
            parts.append(temp_text[:split_pos])
            temp_text = temp_text[split_pos:].lstrip()
        else:
            parts.append(temp_text)
            break
    return parts