from PIL import Image, ImageOps
import streamlit as st
import io

# Função para combinar imagem e moldura
def combine_image_with_frame(user_image_path, frame_image_path):
    # Carregar as imagens
    user_image = Image.open(user_image_path)
    frame_image = Image.open(frame_image_path).convert("RGBA")  # Converter moldura para RGBA

    # Redimensionar a imagem do usuário para caber na moldura
    user_image = ImageOps.fit(user_image, frame_image.size, method=0, bleed=0.0, centering=(0.5, 0.5))

    # Converter a imagem do usuário para RGBA também
    user_image = user_image.convert("RGBA")

    # Sobrepor a imagem do usuário na moldura
    combined_image = Image.alpha_composite(user_image, frame_image)

    return combined_image

# Interface com Streamlit
st.title("Combinar Imagem com Moldura")

# Upload da imagem do usuário
uploaded_file = st.file_uploader("Escolha sua foto", type=["jpg", "png"])

# Se a imagem foi carregada
if uploaded_file is not None:
    # Caminhos das imagens
    frame_image_path = 'FOTO-PERFIL.png'  # Certifique-se de que essa seja a moldura correta

    # Salvar a imagem do usuário
    user_image_path = 'user_image.png'
    with open(user_image_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())

    # Combinar a imagem do usuário com a moldura
    result_image = combine_image_with_frame(user_image_path, frame_image_path)

    # Exibir a imagem resultante
    st.image(result_image, caption='Imagem combinada com moldura')

    # Converter a imagem combinada em bytes
    img_byte_arr = io.BytesIO()
    result_image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    # Adicionar um botão para baixar a imagem
    st.download_button(
        label="Baixar Imagem",
        data=img_byte_arr,
        file_name="imagem_com_moldura.png",
        mime="image/png"
    )
