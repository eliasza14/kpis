import streamlit as st

def main():
    st.sidebar.title("Menu")
    
    with st.sidebar.beta_expander("ad"):
        st.write("-> 2")
        st.write("-> 3")

    with st.sidebar.beta_expander("e"):
        st.write("-> 2")
        st.write("-> 5")

    st.sidebar.write("pinkas")

if __name__ == "__main__":
    main()

