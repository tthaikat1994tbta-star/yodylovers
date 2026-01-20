import sys

# Thiết lập encoding cho stdout ngay lập tức
if sys.stdout.encoding != 'utf-8':
    try:
        import codecs
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    except:
        pass

def add_yody_product():
    data = {
        "ten": "Áo Phao Nữ Yody Mũ Ẩn 4S.Plus Siêu Nhẹ Giữ Ấm Chống Gió Hiệu Quả TRA WCPJ25F011",
        "gia": "699.000đ",
        "anh": "https://down-vn.img.susercontent.com/file/vn-11134207-7r98o-m49n0v5u8l0m5c",
        "link": "https://shopee.vn/%C3%81o-Phao-N%E1%BB%AF-Yody-M%C5%A9-%E1%BA%A8n-4S.Plus-Si%C3%AAu-Nh%E1%BA%B9-Gi%E1%BB%AF-%E1%BA%A4m-Ch%E1%BB%91ng-Gi%C3%B3-Hi%E1%BB%87u-Qu%E1%BA%A3-TRA-WCPJ25F011-i.173392916.49400303939"
    }

    html_path = "index.html"
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()

        new_product_html = f'''
            <!-- San pham Yody moi them -->
            <div class="bg-white rounded-2xl shadow-md border border-gray-100 flex flex-col h-full">
                <div class="h-80 overflow-hidden relative rounded-t-2xl">
                    <img src="{data['anh']}" class="w-full h-full object-cover">
                    <span class="absolute top-2 left-2 bg-red-500 text-white text-[10px] font-bold px-2 py-1 rounded-full uppercase">🔥 NEW</span>
                </div>
                <div class="p-4 flex flex-col flex-grow">
                    <h2 class="text-sm font-bold text-[#152b49] mb-2 h-10 overflow-hidden line-clamp-2">{data['ten']}</h2>
                    <div class="mt-auto">
                        <p class="text-red-600 font-black text-xl mb-3">{data['gia']}</p>
                        <a href="{data['link']}" target="_blank" class="block w-full text-center bg-[#fcaf17] text-[#152b49] py-2.5 rounded-xl font-black text-xs uppercase hover:bg-[#152b49] hover:text-white transition-all">Mua Ngay</a>
                    </div>
                </div>
            </div>
'''
        
        marker = '<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">'
        if marker in content:
            parts = content.split(marker)
            updated_content = parts[0] + marker + new_product_html + parts[1]
            
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print("Da cap nhat file index.html thanh cong!")
        else:
            print("Khong tim thay vi tri chen.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    add_yody_product()
