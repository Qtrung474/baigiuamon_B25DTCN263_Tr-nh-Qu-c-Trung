import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, 'data.json')

def classify_grade(average_score):
    if average_score < 5.0: 
        return "Yeu"
    elif 5.0 <= average_score < 7.0: 
        return "TB"
    elif 7.0 <= average_score < 8.0: 
        return "Kha"
    else: 
        return "Gioi"

def calculate_average(math, physics, chemistry):
    return round((math + physics + chemistry) / 3, 2)

def display_student_list(student_list):
    if not student_list:
        print("Danh sách trống!")
        return
    print("-" * 85)
    print(f"| {'ID':<7} | {'Student Name':<20} | {'Math':<5} | {'Phys':<5} | {'Chem':<5} | {'Avg':<5} | {'Grade':<8} |")
    print("-" * 85)
    for student in student_list:
        print(f"| {student['id']:<7} | {student['name']:<20} | {student['math_score']:<5} | {student['physics_score']:<5} | {student['chemistry_score']:<5} | {student['average_score']:<5} | {student['classification']:<8} |")
    print("-" * 85)

def input_score(subject_name):
    while True:
        try:
            score = float(input(f"Nhập điểm {subject_name} (0-10): "))
            if 0 <= score <= 10:
                return score
            else:
                print("Lỗi: Điểm phải nằm trong khoảng từ 0 đến 10!")
        except ValueError:
            print("Lỗi: Vui lòng nhập một số hợp lệ!")

def save_to_json(student_list):
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(student_list, f, indent=4, ensure_ascii=False)

def load_and_display_students():
    student_list = []
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            try:
                student_list = json.load(f)
                print("\n[Đọc dữ liệu từ data.json thành công]")
            except:
                student_list = []
    else:
        print("\n[Không tìm thấy file data.json, tạo danh sách trống]")
    
    display_student_list(student_list)
    return student_list

def add_student(student_list):
    print("\n--- THÊM SINH VIÊN ---")
    while True:
        student_id = input("Nhập Mã SV: ").strip()
        if any(student['id'] == student_id for student in student_list):
            print("Lỗi: Mã SV đã tồn tại. Vui lòng nhập mã khác!")
        else:
            break
            
    name = input("Nhập tên SV: ").strip()
    math_score = input_score("Toán")
    physics_score = input_score("Lý")
    chemistry_score = input_score("Hóa")
    
    average_score = calculate_average(math_score, physics_score, chemistry_score)
    classification = classify_grade(average_score)
    
    new_student = {
        "id": student_id,
        "name": name,
        "math_score": math_score,
        "physics_score": physics_score,
        "chemistry_score": chemistry_score,
        "average_score": average_score,
        "classification": classification
    }
    student_list.append(new_student)
    save_to_json(student_list)
    print("-> Thêm sinh viên thành công!")

def update_student(student_list):
    print("\n--- CẬP NHẬT THÔNG TIN ---")
    student_id = input("Nhập Mã SV cần cập nhật: ").strip()
    for student in student_list:
        if student['id'] == student_id:
            print(f"Tìm thấy sinh viên: {student['name']}")
            student['math_score'] = input_score("Toán mới")
            student['physics_score'] = input_score("Lý mới")
            student['chemistry_score'] = input_score("Hóa mới")
            
            student['average_score'] = calculate_average(student['math_score'], student['physics_score'], student['chemistry_score'])
            student['classification'] = classify_grade(student['average_score'])
            
            save_to_json(student_list)
            print("-> Cập nhật thành công!")
            return
    print("-> Không tìm thấy mã SV này!")

def delete_student(student_list):
    print("\n--- XÓA SINH VIÊN ---")
    student_id = input("Nhập Mã SV cần xóa: ").strip()
    for student in student_list:
        if student['id'] == student_id:
            confirm = input(f"Bạn có chắc muốn xóa SV {student['name']}? (y/n): ").strip().lower()
            if confirm == 'y':
                student_list.remove(student)
                save_to_json(student_list)
                print("-> Đã xóa thành công!")
            else:
                print("-> Đã hủy thao tác xóa.")
            return
    print("-> Không tìm thấy mã SV này!")

def search_student(student_list):
    print("\n--- TÌM KIẾM SINH VIÊN ---")
    keyword = input("Nhập Mã SV hoặc Tên cần tìm: ").strip().lower()
    results = []
    for student in student_list:
        if keyword == student['id'].lower() or keyword in student['name'].lower():
            results.append(student)
    
    if results:
        print(f"Tìm thấy {len(results)} kết quả:")
        display_student_list(results)
    else:
        print("-> Không tìm thấy sinh viên nào phù hợp!")

def sort_students(student_list):
    print("\n--- SẮP XẾP DANH SÁCH ---")
    print("1. Sắp xếp theo Điểm TB giảm dần")
    print("2. Sắp xếp theo Tên tăng dần (A-Z)")
    choice = input("Chọn kiểu sắp xếp (1/2): ")
    
    if choice == '1':
        student_list.sort(key=lambda x: x['average_score'], reverse=True)
        print("-> Đã sắp xếp theo Điểm TB giảm dần.")
    elif choice == '2':
        student_list.sort(key=lambda x: x['name'])
        print("-> Đã sắp xếp theo Tên tăng dần.")
    else:
        print("Lựa chọn không hợp lệ!")
        return
    
    save_to_json(student_list)
    display_student_list(student_list)

def grade_statistics(student_list):
    print("\n--- THỐNG KÊ HỌC LỰC ---")
    stats = {"Gioi": 0, "Kha": 0, "TB": 0, "Yeu": 0}
    for student in student_list:
        grade = student['classification']
        if grade in stats:
            stats[grade] += 1
            
    print(f"Số sinh viên Giỏi: {stats['Gioi']}")
    print(f"Số sinh viên Khá : {stats['Kha']}")
    print(f"Số sinh viên TB  : {stats['TB']}")
    print(f"Số sinh viên Yếu : {stats['Yeu']}")

def display_max_min_average(student_list):
    if not student_list:
        print("Danh sách trống!")
        return
    
    print("\n--- SV ĐIỂM TB CAO NHẤT / THẤP NHẤT ---")
    max_avg = max(student['average_score'] for student in student_list)
    min_avg = min(student['average_score'] for student in student_list)
    
    print(f"\n[Sinh viên có điểm TB CAO NHẤT] ({max_avg} điểm):")
    students_max = [s for s in student_list if s['average_score'] == max_avg]
    display_student_list(students_max)
    
    print(f"\n[Sinh viên có điểm TB THẤP NHẤT] ({min_avg} điểm):")
    students_min = [s for s in student_list if s['average_score'] == min_avg]
    display_student_list(students_min)

def reclassify_all_students(student_list):
    print("\n--- KIỂM TRA PHÂN LOẠI HỌC LỰC ---")
    print("Hệ thống đang quét lại toàn bộ danh sách để đảm bảo tính chính xác...")
    for student in student_list:
        student['classification'] = classify_grade(student['average_score'])
        
    save_to_json(student_list)
    print("-> Đã cập nhật và phân loại lại học lực cho toàn bộ sinh viên!")
    display_student_list(student_list)

def main():
    student_list = []
    
    while True:
        print("\n" + "="*35)
        print("   QUẢN LÝ DANH SÁCH SINH VIÊN")
        print("="*35)
        print("1. Hiển thị danh sách sinh viên")
        print("2. Thêm mới sinh viên")
        print("3. Cập nhật thông tin sinh viên")
        print("4. Xóa sinh viên")
        print("5. Tìm kiếm sinh viên")
        print("6. Sắp xếp danh sách sinh viên")
        print("7. Thống kê điểm TB")
        print("8. Liệt kê sinh viên có điểm TB Max/Min")
        print("9. Phân loại học lực sinh viên")
        print("10. Thoát")
        print("="*35)
        
        choice = input("Chọn chức năng (1-10): ")
        
        if choice == '1':
            student_list = load_and_display_students()
        elif choice == '10':
            print("Đã thoát chương trình. Tạm biệt!")
            break
        else:
            if not student_list and os.path.exists(FILE_PATH):
                with open(FILE_PATH, 'r', encoding='utf-8') as f:
                    try: 
                        student_list = json.load(f)
                    except: 
                        student_list = []
            
            if choice == '2': add_student(student_list)
            elif choice == '3': update_student(student_list)
            elif choice == '4': delete_student(student_list)
            elif choice == '5': search_student(student_list)
            elif choice == '6': sort_students(student_list)
            elif choice == '7': grade_statistics(student_list)
            elif choice == '8': display_max_min_average(student_list)
            elif choice == '9': reclassify_all_students(student_list)
            else: print("Lựa chọn không hợp lệ, vui lòng chọn từ 1-10.")

if __name__ == '__main__':
    main()
