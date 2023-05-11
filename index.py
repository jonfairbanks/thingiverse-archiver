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
    st.title("Thingiverse Collection Archiver")
    with st.form("url_form"):
        url = st.text_input("Enter a URL:", placeholder="https://www.thingiverse.com/<username>/collections/<collection_id>/things")
        submit_button = st.form_submit_button("Archive")
        zip_path = None  # Default value for zip_path
        if submit_button and url:
            url_pattern = re.compile(r'^https://www.thingiverse.com/\w+/collections/\w+/things$')
            if url_pattern.match(url):
                collection_id = re.search(r"/collections/(\d+)/", url).group(1)
                with st.spinner("Generating archive..."):
                    file_path = archiver.download_collection(url)
                    zip_path = archiver.archive_collection(collection_id)
            else:
                st.write("Please enter a valid Thingiverse collection URL")
    if zip_path is not None:
        with open(zip_path, "rb") as fp:
            btn = st.download_button(
                label="Save Archive",
                data=fp,
                file_name=f"{zip_path}",
                mime="application/zip"
            )

if __name__ == "__main__":
    main()
