import cv2
import streamlit as st

import albumentations as A

from . import param2func
from . import get_images_list, load_image, upload_image


def select_image(col, path_to_images: str, interface_type: str = "Simple"):
    """Show interface to choose the image, and load it
    Args:
        path_to_images (dict): path ot folder with images
        interface_type (dict): mode of the interface used
    Returns:
        (status, image)
        status (int):
            0 - if everything is ok
            1 - if there is error during loading of image file
            2 - if user hasn't uploaded photo yet
    """
    image_names_list = get_images_list(path_to_images)
    if len(image_names_list) < 1:
        return 1, 0, None
    else:
        if interface_type == "Professional":
            image_name = st.sidebar.selectbox(
                "Select an image:", image_names_list + ["Upload my image"]
            )
        else:
            image_name = st.sidebar.selectbox("Select an image:", image_names_list)

        if image_name != "Upload my image":
            try:
                image = load_image(image_name, path_to_images)
                return 0, image, image_name
            except cv2.error:
                return 1, 0, None
        else:
            try:
                image = upload_image(col)
                return 0, image, "uploaded.jpg"
            except cv2.error:
                return 1, 0, None
            except AttributeError:
                return 2, 0, None


def show_transform_control(transform_params: dict, n_for_hash: int) -> dict:
    param_values = {"p": 1.0}
    if len(transform_params) == 0:
        st.sidebar.text("Transform has no parameters")
    else:
        for param in transform_params:
            control_function = param2func[param["type"]]
            if isinstance(param["param_name"], list):
                returned_values = control_function(**param, n_for_hash=n_for_hash)
                for name, value in zip(param["param_name"], returned_values):
                    param_values[name] = value
            else:
                param_values[param["param_name"]] = control_function(
                    **param, n_for_hash=n_for_hash
                )
    return param_values


def get_transormations_params(transform_names: list, augmentations: dict) -> list:
    transforms = []
    for i, transform_name in enumerate(transform_names):
        # select the params values
        st.sidebar.subheader("Params of the " + transform_name)
        param_values = show_transform_control(augmentations[transform_name], i)
        transforms.append(getattr(A, transform_name)(**param_values))
    return transforms
