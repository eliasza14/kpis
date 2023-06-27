import streamlit as st





def main():
    st.write(home())
    st.sidebar.title("Menu")
    
    selected_item = st.sidebar.selectbox("", ["ad", "e", "pinkas"])
    
    if selected_item == "ad":
        display_ad_submenu()
    elif selected_item == "e":
        display_e_submenu()
    elif selected_item == "pinkas":
        display_pinkas_submenu()

def display_ad_submenu():
    st.subheader("ad Submenu")
    ad_options = ["2", "3"]
    selected_option = st.selectbox("Select an option", ad_options)
    
    if selected_option == "2":
        st.write("Content for Option 2 in ad submenu")
        # Add content for Option 2 in ad submenu here
    elif selected_option == "3":
        st.write("Content for Option 3 in ad submenu")
        # Add content for Option 3 in ad submenu here

def display_e_submenu():
    st.subheader("e Submenu")
    e_options = ["2", "5"]
    selected_option = st.selectbox("Select an option", e_options)
    
    if selected_option == "2":
        st.write("Content for Option 2 in e submenu")
        # Add content for Option 2 in e submenu here
    elif selected_option == "5":
        st.write("Content for Option 5 in e submenu")
        # Add content for Option 5 in e submenu here

def display_pinkas_submenu():
    st.subheader("pinkas Submenu")
    st.write("Content for pinkas submenu")
    # Add content for pinkas submenu here




def home():
    query_params = st.experimental_get_query_params()
    id_received = query_params.get("id", [""])[0]
    
    id_input = st.text_input("Enter ID", value=id_received)
    if id_input:
        display_contents(id_input)

def display_contents(id_received):
    # Retrieve the contents of the specific ID (replace with your own logic)
    contents = {'id': id_received, 'name': 'John eseaas', 'email': 'john@example.com'}

    st.write(f'# Contents of ID: {id_received}')
    st.write(f'Name: {contents["name"]}')
    st.write(f'Email: {contents["email"]}')



if __name__ == "__main__":
    main()
    
