import sys
from playwright.sync_api import sync_playwright

# Cấu hình encoding cho terminal Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def get_shopee_info(url):
    print(f"--- Đang bắt đầu lấy thông tin ---")
    with sync_playwright() as p:
        # Khởi chạy trình duyệt
        browser = p.chromium.launch(headless=True)
        # Giả lập thiết bị để tránh bị chặn
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 800}
        )
        page = context.new_page()
        
        print(f"Đang truy cập: {url}")
        result = None
        try:
            page.goto(url, wait_until="networkidle", timeout=60000)
            
            # Đợi các thành phần quan trọng hiển thị
            page.wait_for_timeout(5000) 
            
            # Lấy tên sản phẩm từ tiêu đề trang hoặc selector
            ten_sp = page.title().split(" | ")[0]
            
            # Selector cho Shopee (thường thay đổi, dùng nhiều phương án)
            gia_sp = "Liên hệ"
            price_selectors = ['div.pqm66B', 'div.flex.items-center > div.font-medium', '.G27LRz', 'span.G27LRz']
            for selector in price_selectors:
                try:
                    element = page.query_selector(selector)
                    if element:
                        gia_sp = element.inner_text()
                        break
                except:
                    continue

            # Lấy ảnh sản phẩm
            anh_sp = ""
            image_selectors = ['div.pCOp9a > img', 'img.B6997U', 'img._89\+v8Y']
            for selector in image_selectors:
                try:
                    element = page.query_selector(selector)
                    if element:
                        anh_sp = element.get_attribute('src')
                        break
                except:
                    continue

            if "Đăng nhập" in ten_sp:
                print("Cảnh báo: Bị chặn bởi trang đăng nhập Shopee.")
            
            result = {
                "ten": ten_sp,
                "gia": gia_sp,
                "anh": anh_sp,
                "link": url
            }
            
            print(f"Thành công!")
            print(f"Tên: {ten_sp}")
            print(f"Giá: {gia_sp}")
            print(f"Ảnh: {anh_sp}")

        except Exception as e:
            print(f"Lỗi khi cào dữ liệu: {e}")

        browser.close()
        return result

def update_html(data):
    if not data:
        print("Không có dữ liệu để cập nhật HTML.")
        return

    html_path = "index.html"
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Tạo block HTML mới cho sản phẩm
        new_product_html = f'''
            <!-- Sản phẩm mới từ Shopee -->
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
        
        # Chèn vào trước thẻ đóng div cuối cùng của grid (thẻ đóng grid)
        # Tìm vị trí grid grid-cols-...
        marker = '<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">'
        if marker in content:
            parts = content.split(marker)
            # Chèn ngay sau thẻ mở grid
            updated_content = parts[0] + marker + new_product_html + parts[1]
            
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print(f"Đã cập nhật file {html_path} thành công!")
        else:
            print("Không tìm thấy vị trí chèn trong file HTML.")

    except Exception as e:
        print(f"Lỗi khi cập nhật HTML: {e}")

# Link sản phẩm bạn yêu cầu
link_yeu_cau = "https://shopee.vn/%C3%81o-Phao-N%E1%BB%AF-Yody-M%C5%A9-%E1%BA%A8n-4S.Plus-Si%C3%AAu-Nh%E1%BA%B9-Gi%E1%BB%AF-%E1%BA%A4m-Ch%E1%BB%91ng-Gi%C3%B3-Hi%E1%BB%87u-Qu%E1%BA%A3-TRA-WCPJ25F011-i.173392916.49400303939"

product_data = get_shopee_info(link_yeu_cau)
if product_data:
    update_html(product_data)
