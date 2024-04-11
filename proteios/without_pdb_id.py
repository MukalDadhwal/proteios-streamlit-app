import streamlit as st
from stmol import showmol
import py3Dmol
import requests
import biotite.structure.io as bsio
import py3Dmol
from Bio import PDB
import matplotlib.pyplot as plt
from graphein.protein.analysis import plot_residue_composition
from graphein.protein.graphs import construct_graph
from graphein.protein.config import ProteinGraphConfig, DSSPConfig
from graphein.protein.edges.distance import (
    add_aromatic_interactions,
    add_disulfide_interactions,
    add_hydrophobic_interactions,
    add_peptide_bonds,
)
from graphein.protein.visualisation import plotly_protein_structure_graph
from graphein.protein.analysis import plot_edge_type_distribution

tab1, tab2, tab3 = st.tabs(["3-D Model Visualization", "Insights", "About the Project"])


st.sidebar.title('Proteios')

st.sidebar.write('La La La') #sidebar paragraph replace with meaningful things

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


def generate_visual_graphein(pdb_file):
    config = ProteinGraphConfig(
     edge_construction_functions=[       # List of functions to call to construct edges.
         add_hydrophobic_interactions,
         add_aromatic_interactions,
         add_disulfide_interactions,
         add_peptide_bonds,
     ],
     #graph_metadata_functions=[asa, rsa],  # Add ASA and RSA features.
     #dssp_config=DSSPConfig(),             # Add DSSP config in order to compute ASA and RSA.
    )  
    g = construct_graph(path=pdb_file, config=config)

    return g


# Protein sequence input
DEFAULT_SEQ = "MGSSHHHHHHSSGLVPRGSHMRGPNPTAASLEASAGPFTVRSFTVSRPSGYGAGTVYYPTNAGGTVGAIAIVPGYTARQSSIKWWGPRLASHGFVVITIDTNSTLDQPSSRSSQQMAALRQVASLNGTSSSPIYGKVDTARMGVMGWSMGGGGSLISAANNPSLKAAAPQAPWDSSTNFSSVTVPTLIFACENDSIAPVNSSALPIYDSMSRNAKQFLEINGGSHSCANSGNSNQALIGKKGVAWMKRFMDNDTRYSTFACENPNSTRVSDFRTANCSLEDPAANKARKEAELAAATAEQ"
txt = st.sidebar.text_area('Input sequence', DEFAULT_SEQ, height=275)

# ESMfold
def update(sequence=txt):
    with tab1:
   
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        response = requests.post('https://api.esmatlas.com/foldSequence/v1/pdb/', headers=headers, data=sequence,verify = False)
        name = sequence[:3] + sequence[-3:]
        pdb_string = response.content.decode('utf-8')

        #with open('predicted.pdb', 'w') as f:
        #   f.write(pdb_string)

        f ="predicted.pdb"

        g = generate_visual_graphein(f)
        
        struct = bsio.load_structure('predicted.pdb', extra_fields=["b_factor"])
        b_value = round(struct.b_factor.mean(), 4)

        st.subheader('Visualization of predicted protein structure')
        #render_mol(pdb_string)
        st.write(plotly_protein_structure_graph(g, node_size_multiplier=1))

        st.subheader('plDDT')
        st.write('plDDT is a per-residue estimate of the confidence in prediction on a scale from 0-100.')
        st.info(f'plDDT: {b_value}')

        st.download_button(
            label="Download PDB",
            data=pdb_string,
            file_name='predicted.pdb',
            mime='text/plain',
        )

        return g


graph = update()

predict = st.sidebar.button('Predict', on_click=update)

#if not predict:
  #          st.warning('👈 Enter protein sequence data!')


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


with tab2:
    fig = plot_residue_composition(graph, sort_by="count", plot_type="pie") # Can also sort by "alphabetical"
    st.write(fig)

    fig2 = plot_edge_type_distribution(graph, plot_type="bar", title="Edge Type Distribution")
    st.write(fig2)


with tab3:
    about_us()





    

