import streamlit as st
from stmol import showmol
import py3Dmol
import requests
import biotite.structure.io as bsio

tab1, tab2, tab3 = st.tabs(["3-D Model Visualization", "Insights", "About the Project"])

st.sidebar.title('Proteios')

st.sidebar.write('[*ESMFold*](https://esmatlas.com/about) is an end-to-end single sequence protein structure predictor based on the ESM-2 language model. For more information, read the [research article](https://www.biorxiv.org/content/10.1101/2022.07.20.500902v2) and the [news article](https://www.nature.com/articles/d41586-022-03539-1) published in *Nature*.')

# stmol
def render_mol(pdb):
    pdbview = py3Dmol.view()
    pdbview.addModel(pdb,'pdb')
    pdbview.setStyle({'cartoon':{'color':'spectrum'}})
    pdbview.setBackgroundColor('white')#('0xeeeeee')
    pdbview.zoomTo()
    pdbview.zoom(2, 800)
    pdbview.spin(True)
    showmol(pdbview, height = 500,width=800)

# Protein sequence input
DEFAULT_SEQ = "MGSSHHHHHHSSGLVPRGSHMRGPNPTAASLEASAGPFTVRSFTVSRPSGYGAGTVYYPTNAGGTVGAIAIVPGYTARQSSIKWWGPRLASHGFVVITIDTNSTLDQPSSRSSQQMAALRQVASLNGTSSSPIYGKVDTARMGVMGWSMGGGGSLISAANNPSLKAAAPQAPWDSSTNFSSVTVPTLIFACENDSIAPVNSSALPIYDSMSRNAKQFLEINGGSHSCANSGNSNQALIGKKGVAWMKRFMDNDTRYSTFACENPNSTRVSDFRTANCSLEDPAANKARKEAELAAATAEQ"
txt = st.sidebar.text_area('Input sequence', DEFAULT_SEQ, height=275)

# ESMfold
def update(sequence=txt):
    with tab1:
        if not predict:
            st.warning('👈 Enter protein sequence data!')
            
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        response = requests.post('https://api.esmatlas.com/foldSequence/v1/pdb/', headers=headers, data=sequence,verify = False)
        name = sequence[:3] + sequence[-3:]
        pdb_string = response.content.decode('utf-8')

        with open('predicted.pdb', 'w') as f:
            f.write(pdb_string)

        struct = bsio.load_structure('predicted.pdb', extra_fields=["b_factor"])
        b_value = round(struct.b_factor.mean(), 4)

        st.subheader('Visualization of predicted protein structure')
        render_mol(pdb_string)

        st.subheader('plDDT')
        st.write('plDDT is a per-residue estimate of the confidence in prediction on a scale from 0-100.')
        st.info(f'plDDT: {b_value}')

        st.download_button(
            label="Download PDB",
            data=pdb_string,
            file_name='predicted.pdb',
            mime='text/plain',
        )

predict = st.sidebar.button('Predict', on_click=update)


def about_us():
    st.title("Proteios: A Protein Behavior Prediction Web Application")
    st.write("""
    This web application predicts and visualizes the behavior of known and unknown proteins.
    It utilizes Graphene and BioPython modules to generate 3D views of proteins and provide in-depth information about their structure and constituents.
    """)

    st.header("Mukal Dhadhwal:")
    st.write("""
    LinkedIn: [Mukal's Link](https://www.linkedin.com/in/mukal-dadhwal/)
    """)

    st.header("Brahamdeep Singh.")
    st.write("""
    LinkedIn: [Brahamdeep's Link](https://www.linkedin.com/in/brahamdeep-singh-sabharwal-14a914256/)
    """)

    st.header("Ishwardeep Singh.")
    st.write("""
    LinkedIn: [Ishwardeep's Link](https://www.linkedin.com/in/ishwardeep-singh-405a9324a/)
    """)

    st.header("Prabhsurat Singh.")
    st.write("""
    LinkedIn: [Prabhsurat's Link](https://www.linkedin.com/in/prabhsurat-singh-1868052ab/)
    """)

with tab3:
    about_us()

    

