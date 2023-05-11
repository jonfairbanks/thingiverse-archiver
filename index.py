import archiver
import re
import streamlit as st

# Set Streamlit theme to dark mode
st.set_page_config(
    page_title="Thingiverse Collection Archiver",
    layout="wide",
    initial_sidebar_state="auto"
)

# Hide the Streamlit footer
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

def main():
    st.title("Thingiverse Collection Archiver") # TODO: Figure out how to disable the link option
    st.write("Provide a Thingiverse collection and we’ll extract all of the items into an easily downloadable .zip archive")
    with st.form("url_form"):
        url = st.text_input("Enter a URL:", placeholder="https://www.thingiverse.com/<username>/collections/<collection_id>/things")
        submit_button = st.form_submit_button("Archive")
        zip_path = None  # Default value for zip_path
        if submit_button and url:
            url_pattern = re.compile(r'^https://www.thingiverse.com/\w+/collections/\w+/things$')
            if url_pattern.match(url):
                collection_id = re.search(r"/collections/(\d+)/", url).group(1)
                with st.spinner("Generating archive..."): # TODO: If the archive is generating, hide the archive button
                    file_path = archiver.download_collection(url) # TODO: If the file exists, do not download it
                    zip_path = archiver.archive_collection(collection_id)
            else:
                st.write("Please enter a valid Thingiverse collection URL") # TODO: Can this text be red?
    if zip_path is not None:
        with open(zip_path, "rb") as fp:
            btn = st.download_button(
                label="Save Archive",
                data=fp,
                file_name=f"{zip_path}",
                mime="application/zip"
            )

# Add a footer
def footer():
    footer_style = """
        <style>
        .footer {
            text-align: center;
            color: grey;
        }
        </style>
    """
    st.markdown(footer_style, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div class='footer'>This tool is not affiliated with Ultimaker and/or Thingiverse</div>", unsafe_allow_html=True)
    st.markdown("<div class='footer'>Copyright © 2023</div>", unsafe_allow_html=True) # TODO: Do not hardcode the year

if __name__ == "__main__":
    main()
    footer()