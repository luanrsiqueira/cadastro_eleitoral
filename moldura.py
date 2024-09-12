from PIL import Image
import streamlit as st
from io import BytesIO

st.title("Carregar Foto com Moldura")

# Upload da moldura
moldura_file = st.file_uploader("Carregar a imagem da moldura", type=["png", "jpg", "jpeg"])

# Upload da foto de perfil
foto_file = st.file_uploader("Carregar a foto de perfil", type=["png", "jpg", "jpeg"])

# Quando ambos os arquivos forem carregados
if moldura_file and foto_file:
    # Abrir a moldura
    moldura = Image.open(moldura_file)

    # Abrir a foto de perfil
    foto = Image.open(foto_file)

    # Redimensionar a foto de perfil para caber na moldura
    foto_resized = foto.resize((moldura.width, moldura.height))

    # Combinar as imagens sobrepondo a foto na moldura
    combined_image = moldura.copy()
    combined_image.paste(foto_resized, (0, 0), foto_resized)

    # Exibir a imagem resultante no Streamlit
    st.image(combined_image, caption="Foto com Moldura")

    # Botão para baixar a imagem combinada
    buffer = BytesIO()
    combined_image.save(buffer, format="PNG")
    st.download_button(
        label="Baixar Imagem",
        data=buffer,
        file_name="foto_com_moldura.png",
        mime="image/png"
    )
