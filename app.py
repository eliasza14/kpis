import streamlit as st

def main():
    st.sidebar.title("Menu")
    menu_items = ["Item 1", "Item 2", "Item 3"]
    selected_item = st.sidebar.selectbox("", menu_items)

    if selected_item == "Item 1":
        show_item1_submenu()
    elif selected_item == "Item 2":
        show_item2_submenu()
    elif selected_item == "Item 3":
        show_item3_submenu()

def show_item1_submenu():
    st.subheader("Item 1 Submenu")
    # Add content for Item 1 submenu here

def show_item2_submenu():
    st.subheader("Item 2 Submenu")
    # Add content for Item 2 submenu here

def show_item3_submenu():
    st.subheader("Item 3 Submenu")
    # Add content for Item 3 submenu here

if __name__ == "__main__":
    main()
