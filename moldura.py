from PIL import Image, ImageOps
import streamlit as st
import io

# Função para ajustar a imagem automaticamente dentro da moldura e permitir ajustes manuais
def combine_image_with_frame(user_image_path, frame_image_path, x_offset=0, y_offset=0, scale=1.0):
    # Carregar a moldura e a imagem do usuário
    user_image = Image.open(user_image_path)
    frame_image = Image.open(frame_image_path).convert("RGBA")  # Converter moldura para RGBA

    # Redimensionar a imagem do usuário para caber na área da moldura automaticamente
    user_image = ImageOps.fit(user_image, frame_image.size, method=0, bleed=0.0, centering=(0.5, 0.5))

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
    frame_image_path = 'FOTO-PERFIL.png'  # Moldura fixa já fornecida
    
    # Salvar a imagem do usuário
    user_image_path = 'user_image.png'
    with open(user_image_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())

    # Ajustar automaticamente a imagem dentro da moldura
    result_image = combine_image_with_frame(user_image_path, frame_image_path)

    # Exibir a imagem resultante
    st.image(result_image, caption='Imagem combinada com moldura')

    # Exibir sliders para ajuste de posição e escala (se o usuário desejar ajustar manualmente)
    st.header("Ajustes Manuais")
    x_offset = st.slider("Mover para a esquerda/direita", -500, 500, 0)
    y_offset = st.slider("Mover para cima/baixo", -500, 500, 0)
    scale = st.slider("Ajustar tamanho (escala)", 0.5, 2.0, 1.0)

    # Se o usuário ajustar manualmente, recalcular a imagem
    if x_offset != 0 or y_offset != 0 or scale != 1.0:
        result_image = combine_image_with_frame(user_image_path, frame_image_path, x_offset, y_offset, scale)
        st.image(result_image, caption='Imagem ajustada manualmente com moldura')

    # Converter a imagem combinada em bytes para download
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
