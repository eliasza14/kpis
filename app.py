import streamlit as st

def main():
    st.sidebar.title("Menu")
    
    ad_expander = st.sidebar.expander("ad")
    with ad_expander:
        st.write("-> 2")
        st.write("-> 3")

    e_expander = st.sidebar.expander("e")
    with e_expander:
        st.write("-> 2")
        st.write("-> 5")

    st.sidebar.write("pinkas")

if __name__ == "__main__":
    main()