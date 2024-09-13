from PIL import Image, ImageOps
import streamlit as st
import io

# Função para ajustar a imagem dentro da moldura
def combine_image_with_frame(user_image_path, frame_image_path, x_offset, y_offset, scale):
    # Carregar a moldura e a imagem do usuário
    user_image = Image.open(user_image_path)
    frame_image = Image.open(frame_image_path).convert("RGBA")  # Converter moldura para RGBA

    # Ajustar escala da imagem do usuário
    new_size = (int(user_image.size[0] * scale), int(user_image.size[1] * scale))
    user_image = user_image.resize(new_size, Image.LANCZOS)

    # Criar uma nova imagem transparente no tamanho da moldura
    user_image_padded = Image.new("RGBA", frame_image.size)

    # Colocar a imagem do usuário com base nos offsets
    user_image_padded.paste(user_image, (x_offset, y_offset))

    # Sobrepor a imagem do usuário na moldura
    combined_image = Image.alpha_composite(user_image_padded, frame_image)

    return combined_image

# Interface com Streamlit
st.image("logo_patielen.png", width=100)

# Título da página
st.title("Campanha Patielen Ravana")

# Upload da imagem do usuário
uploaded_file = st.file_uploader("Escolha sua foto", type=["jpg", "png"])

# Se a imagem foi carregada
if uploaded_file is not None:
    # Caminho para a moldura
    frame_image_path = '/mnt/data/file-5dPTOMLV17CBarzHgSVvqCQ2'  # Moldura fixa já fornecida
    
    # Salvar a imagem do usuário
    user_image_path = 'user_image.png'
    with open(user_image_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())

    # Adicionar sliders para ajuste de posição e escala
    st.sidebar.header("Ajustes Manuais")
    x_offset = st.sidebar.slider("Mover para a esquerda/direita", -500, 500, 0)
    y_offset = st.sidebar.slider("Mover para cima/baixo", -500, 500, 0)
    scale = st.sidebar.slider("Ajustar tamanho (escala)", 0.5, 2.0, 1.0)

    # Combinar a imagem do usuário com a moldura usando ajustes manuais
    result_image = combine_image_with_frame(user_image_path, frame_image_path, x_offset, y_offset, scale)

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
