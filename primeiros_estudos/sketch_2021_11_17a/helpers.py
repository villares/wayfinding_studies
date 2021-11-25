def is_img_ext(file_name):
    """
    Return True if file_name ends with
    one of the valid_extensions.
    """
    ext = file_name.split('.')[-1]
    valid_extensions = (
        'jpg',
        'png',
        'jpeg',
        'gif',
        'tif',
        'tga',
        #'svg',
    )
    return ext.lower() in valid_extensions
