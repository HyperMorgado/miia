import inspect
import os

def getFileAndLine() -> str:
    """
    Returns the filename and line number of the caller of this function,
    in the form "filename:line". If anything goes wrong, returns an error message.
    """
    try:
        # inspect.stack()[0] is this frame, [1] is getFileAndLine, [2] is its caller
        frame_record = inspect.stack()[2]
        filepath = frame_record.filename
        file_name = os.path.basename(filepath) if filepath else "path-not-detected"
        line_no = frame_record.lineno
        return f"{file_name}:{line_no}"
    except Exception as e:
        return f"(error in get_file_and_line function) - {e}"


def getFileAndLineCaller() -> str:
    """
    Returns the filename and line number of the *grand*-caller
    (two levels up), in the form "filename:line". Falls back to "Unknown:-1".
    """
    try:
        stack = inspect.stack()
        if len(stack) >= 4:
            # [0]: this frame; [1]: getFileAndLineCaller;
            # [2]: whoever called getFileAndLineCaller;
            # [3]: the caller-of-the-caller
            frame_record = stack[3]
            filepath = frame_record.filename
            line_no = frame_record.lineno
            return f"{filepath}:{line_no}"
        else:
            return "Unknown:-1"
    except Exception:
        return "Unknown:-1"