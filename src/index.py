import archiver
import datetime
import re
import streamlit as st

# Set Streamlit theme to dark mode
st.set_page_config(
    page_title="Thingiverse Collection Archiver",
    layout="wide",
    initial_sidebar_state="auto",
)

# Hide anchor links on titles
hide_anchor_link = """
        <style>
        .css-15zrgzn {display: none}
        .css-eczf16 {display: none}
        .css-jn99sy {display: none}
        </style>
        """
st.markdown(hide_anchor_link, unsafe_allow_html=True)

# Hide the Streamlit footer
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def google_analytics():
    st.markdown(
        """
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-**********"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', 'G-**********');
        </script>
    """,
        unsafe_allow_html=True,
    )


def main():
    st.title("Thingiverse Collection Archiver")
    st.write(
        "Provide a Thingiverse collection and we’ll extract all of the items into an easily downloadable .zip archive"
    )
    with st.form("url_form"):
        url = st.text_input(
            "Enter a URL:",
            placeholder="https://www.thingiverse.com/<username>/collections/<collection_id>/things",
        )
        submit_button = st.form_submit_button("Archive")
        zip_path = None  # Default value for zip_path
        if submit_button and url:
            url_pattern = re.compile(
                r"^https://www.thingiverse.com/\w+/collections/\w+/things$"
            )
            if url_pattern.match(url):
                collection_id = re.search(r"/collections/(\d+)/", url).group(1)
                with st.spinner(
                    "Generating archive..."
                ):  # TODO: If the archive is generating, hide the archive button
                    file_path = archiver.download_collection(url)
                    zip_path = archiver.archive_collection(collection_id)
            else:
                st.write(
                    '<span style="color: red;">Please enter a valid Thingiverse collection URL</span>',
                    unsafe_allow_html=True,
                )
    if zip_path is not None:
        with open(zip_path, "rb") as fp:
            btn = st.download_button(
                label="Save Archive",
                data=fp,
                file_name=f"{zip_path}",
                mime="application/zip",
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
    st.markdown(
        "<div class='footer'>This tool is not affiliated with Ultimaker and/or Thingiverse</div>",
        unsafe_allow_html=True,
    )
    copyright = f"<div class='footer'>Copyright © {datetime.datetime.now().year}</div>"
    st.markdown(copyright, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
    footer()
