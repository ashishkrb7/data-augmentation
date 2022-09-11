import os
import streamlit as st
import albumentations as A
from src import (
    load_augmentations_config,
    get_arguments,
    get_placeholder_params,
    select_transformations,
    select_image,
    get_transormations_params,
)
from PIL import Image
from io import BytesIO

img_byte_arr = BytesIO()


PAGE_CONFIG = {
    "page_icon": "🤖",
    "page_title": "Augument",
    "layout": "wide",
    "initial_sidebar_state": "auto",
}
st.set_page_config(**PAGE_CONFIG)

st.markdown(
    """ <style>#MainMenu {visibility: hidden;}footer {visibility: hidden;}header {visibility: hidden;}</style>""",
    unsafe_allow_html=True,
)

# Remove whitespace from the top of the page and sidebar
st.markdown(
    """
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 0rem;
                    padding-right: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 1rem;
                }
        </style>
        """,
    unsafe_allow_html=True,
)


path_st = os.path.abspath(os.path.join(os.path.dirname(__file__), "./.")).replace(
    "\\", "/"
)  # Working directory


def styling_css_call(file_name):
    """To call CSS"""
    try:
        with open(path_st + "/assets/" + file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass


styling_css_call("global.css")

if not os.path.exists(f"{path_st}/images"):
    os.makedirs(f"{path_st}/images")


def main():
    # get CLI params: the path to images and image width
    path_to_images, width_original = get_arguments()

    if not os.path.isdir(path_to_images):
        st.title("There is no directory: " + path_to_images)
    else:
        # select interface type
        interface_type = st.sidebar.radio(
            "Select the interface mode", ["Simple", "Professional"]
        )

        # select image
        status, image, image_name = select_image(st, path_to_images, interface_type)
        if status == 1:
            st.title("Can't load image")
        if status == 2:
            st.title("Please, upload the image")
        else:
            # image was loaded successfully
            placeholder_params = get_placeholder_params(image)

            # load the config
            augmentations = load_augmentations_config(
                placeholder_params, "configs/augmentations.json"
            )

            # get the list of transformations names
            transform_names = select_transformations(augmentations, interface_type)

            # get parameters for each transform
            transforms = get_transormations_params(transform_names, augmentations)

            try:
                # apply the transformation to the image
                data = A.ReplayCompose(transforms)(image=image)
                error = 0
            except ValueError:
                error = 1
                st.title(
                    "The error has occurred. Most probably you have passed wrong set of parameters. \
                Check transforms that change the shape of image."
                )

            # proceed only if everything is ok
            if error == 0:
                augmented_image = data["image"]
                # show title
                st.title("Augmentation Using Albumentation")

                # show the images
                width_transformed = int(
                    width_original / image.shape[1] * augmented_image.shape[1]
                )
                col1, col2 = st.columns(2, gap="small")
                col1.image(image, caption="Original image", width=width_original)
                col2.image(
                    augmented_image,
                    caption="Transformed image",
                    width=width_transformed,
                )

                random_values = {}
                for applied_params in data["replay"]["transforms"]:
                    random_values[
                        applied_params["__class_fullname__"].split(".")[-1]
                    ] = applied_params["params"]

                pilimage = Image.fromarray(augmented_image.astype("uint8"), "RGB")
                pilimage.save(img_byte_arr, format="JPEG")
                byte_im = img_byte_arr.getvalue()
                col2.download_button(
                    label="Download image",
                    data=byte_im,
                    file_name=f"{'_'.join(list(random_values.keys()))}_{image_name}",
                    mime="image/jpeg",
                )

                # print additional info
                for transform in transforms:
                    with st.expander(
                        f"Docstring for {transform.__class__.__name__}", expanded=False
                    ):
                        st.text(transform.__doc__)
                    st.code(str(transform))


if __name__ == "__main__":
    main()
