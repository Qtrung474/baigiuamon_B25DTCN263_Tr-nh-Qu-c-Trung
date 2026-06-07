import json
import os

FILE_NAME = "data.json"
students_list = []

def load_data():
    global students_list
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r', encoding='utf-8') as file:
            students_list = json.load(file)
    else:
        students_list = []

def save_data():
    with open(FILE_NAME, 'w', encoding='utf-8') as file:
        json.dump(students_list, file, ensure_ascii=False, indent=4)

def get_classification(average_score):
    if average_score < 5.0:
        return "Yếu"
    elif 5.0 <= average_score < 7.0:
        return "TB"
    elif 7.0 <= average_score < 8.0:
        return "Khá"
    else:
        return "Giỏi"

def input_score(subject_name):
    while True:
        try:
            score = float(input(f"Nhập điểm {subject_name} (0 - 10): "))
            if 0 <= score <= 10:
                return score
            else:
                print("Lỗi: Điểm phải nằm trong khoảng từ 0 đến 10!")
        except ValueError:
            print("Lỗi: Vui lòng nhập một số hợp lệ!")

def print_table(students):
    if not students:
        print("Danh sách trống!")
        return
    
    print("-" * 88)
    print(f"| {'Mã SV':<7} | {'Họ và Tên':<20} | {'Toán':<5} | {'Lý':<5} | {'Hóa':<5} | {'Điểm TB':<7} | {'Xếp loại':<10} |")
    print("-" * 88)
    for student in students:
        print(f"| {student['id']:<7} | {student['name']:<20} | {student['math_score']:<5.1f} | {student['physics_score']:<5.1f} | {student['chemistry_score']:<5.1f} | {student['average_score']:<7.2f} | {student['classification']:<10} |")
    print("-" * 88)

def display_students():
    print("\n--- 1. HIỂN THỊ DANH SÁCH SINH VIÊN ---")
    load_data() 
    print_table(students_list)

def add_student():
    print("\n--- 2. THÊM MỚI SINH VIÊN ---")
    student_id = input("Nhập Mã SV: ").strip()
    
    for student in students_list:
        if student['id'] == student_id:
            print("Lỗi: Mã sinh viên đã tồn tại!")
            return

    student_name = input("Nhập tên sinh viên: ").strip()
    math_score = input_score("Toán")
    physics_score = input_score("Lý")
    chemistry_score = input_score("Hóa")
    
    average_score = round((math_score + physics_score + chemistry_score) / 3, 2)
    classification = get_classification(average_score)
    
    new_student = {
        "id": student_id,
        "name": student_name,
        "math_score": math_score,
        "physics_score": physics_score,
        "chemistry_score": chemistry_score,
        "average_score": average_score,
        "classification": classification
    }
    
    students_list.append(new_student)
    save_data()
    print("-> Đã thêm sinh viên thành công!")

def update_student():
    print("\n--- 3. CẬP NHẬT THÔNG TIN SINH VIÊN ---")
    student_id = input("Nhập Mã SV cần cập nhật: ").strip()
    
    for student in students_list:
        if student['id'] == student_id:
            print(f"Đang cập nhật điểm cho sinh viên: {student['name']}")
            student['math_score'] = input_score("Toán")
            student['physics_score'] = input_score("Lý")
            student['chemistry_score'] = input_score("Hóa")
            
            student['average_score'] = round((student['math_score'] + student['physics_score'] + student['chemistry_score']) / 3, 2)
            student['classification'] = get_classification(student['average_score'])
            
            save_data()
            print("-> Cập nhật thành công!")
            return
            
    print("Lỗi: Không tìm thấy Mã SV này!")

def delete_student():
    print("\n--- 4. XÓA SINH VIÊN ---")
    student_id = input("Nhập Mã SV cần xóa: ").strip()
    
    for i in range(len(students_list)):
        if students_list[i]['id'] == student_id:
            confirm = input(f"Bạn có chắc muốn xóa sinh viên {students_list[i]['name']}? (y/n): ")
            if confirm.lower() == 'y':
                del students_list[i] 
                save_data()
                print("-> Đã xóa thành công!")
            else:
                print("-> Đã hủy thao tác xóa.")
            return
            
    print("Lỗi: Không tìm thấy Mã SV này!")

def search_student():
    print("\n--- 5. TÌM KIẾM SINH VIÊN ---")
    keyword = input("Nhập Mã SV hoặc Tên để tìm: ").strip().lower()
    
    search_results = []
    for student in students_list:
        if keyword in student['id'].lower() or keyword in student['name'].lower():
            search_results.append(student)
            
    if search_results:
        print(f"-> Tìm thấy {len(search_results)} kết quả:")
        print_table(search_results)
    else:
        print("-> Không tìm thấy sinh viên nào phù hợp.")

def sort_students():
    print("\n--- 6. SẮP XẾP DANH SÁCH ---")
    print("1. Sắp xếp theo Điểm TB (Giảm dần)")
    print("2. Sắp xếp theo Tên (A-Z)")
    choice = input("Chọn cách sắp xếp (1/2): ")
    
    if choice == '1':
        students_list.sort(key=lambda x: x['average_score'], reverse=True)
        print("-> Đã sắp xếp theo Điểm TB giảm dần.")
        print_table(students_list)
        save_data()
    elif choice == '2':
        students_list.sort(key=lambda x: x['name'])
        print("-> Đã sắp xếp theo Tên tăng dần.")
        print_table(students_list)
        save_data()
    else:
        print("Lựa chọn không hợp lệ!")

def show_statistics():
    print("\n--- 7. THỐNG KÊ ĐIỂM TB ---")
    stats = {"Giỏi": 0, "Khá": 0, "TB": 0, "Yếu": 0}
    
    for student in students_list:
        rank = student['classification']
        if rank in stats:
            stats[rank] += 1
            
    print(f"Số SV loại Giỏi: {stats['Giỏi']}")
    print(f"Số SV loại Khá:  {stats['Khá']}")
    print(f"Số SV loại TB:   {stats['TB']}")
    print(f"Số SV loại Yếu:  {stats['Yếu']}")

def find_extreme_scores():
    print("\n--- 8. SINH VIÊN CÓ ĐIỂM TB CAO NHẤT / THẤP NHẤT ---")
    if not students_list:
        print("Danh sách trống!")
        return
        
    max_score = max(student['average_score'] for student in students_list)
    min_score = min(student['average_score'] for student in students_list)
    
    top_students = [student for student in students_list if student['average_score'] == max_score]
    bottom_students = [student for student in students_list if student['average_score'] == min_score]
    
    print("\n*** NHỮNG SINH VIÊN CÓ ĐIỂM TB CAO NHẤT ***")
    print_table(top_students)
    
    print("\n*** NHỮNG SINH VIÊN CÓ ĐIỂM TB THẤP NHẤT ***")
    print_table(bottom_students)

def display_classifications():
    print("\n--- 9. PHÂN LOẠI HỌC LỰC SINH VIÊN ---")
    print("Tiêu chí phân loại:")
    print(" - Điểm TB < 5.0      : Yếu")
    print(" - Điểm TB [5.0 - 7.0): Trung Bình")
    print(" - Điểm TB [7.0 - 8.0): Khá")
    print(" - Điểm TB [8.0 - 10] : Giỏi")
    print("\nDanh sách chi tiết theo xếp loại:")
    print_table(students_list)

load_data()

while True:
    print("\n" + "="*45)
    print("      CHƯƠNG TRÌNH QUẢN LÝ SINH VIÊN")
    print("="*45)
    print("1. Hiển thị danh sách sinh viên")
    print("2. Thêm mới sinh viên")
    print("3. Cập nhật thông tin sinh viên")
    print("4. Xóa sinh viên")
    print("5. Tìm kiếm sinh viên")
    print("6. Sắp xếp danh sách sinh viên")
    print("7. Thống kê điểm TB")
    print("8. Liệt kê SV điểm TB cao nhất/thấp nhất")
    print("9. Phân loại học lực sinh viên")
    print("10. Thoát")
    print("="*45)
    
    user_choice = input("Nhập lựa chọn của bạn (1-10): ")
    
    if user_choice == '1':
        display_students()
    elif user_choice == '2':
        add_student()
    elif user_choice == '3':
        update_student()
    elif user_choice == '4':
        delete_student()
    elif user_choice == '5':
        search_student()
    elif user_choice == '6':
        sort_students()
    elif user_choice == '7':
        show_statistics()
    elif user_choice == '8':
        find_extreme_scores()
    elif user_choice == '9':
        display_classifications()
    elif user_choice == '10':
        save_data()
        print("Đã thoát chương trình. Tạm biệt!")
        break
    else:
        print("Lựa chọn không hợp lệ, vui lòng nhập lại!")