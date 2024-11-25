# Cơ sở dữ liệu thô chứa các thông tin về thời gian khởi hành, thời gian đến, thời gian chạy và phương tiện.
raw_database = [
    """(DTIME PQ HCMC "7AM 1/7")""",
    """(ATIME PQ PQ "9AM 1/7")""",
    """(DTIME PQ HCMC "8AM 5/7")""",
    """(ATIME PQ PQ "10AM 5/7")""",
    """(DTIME DN HCMC "7AM 1/7")""",
    """(ATIME DN DN "9AM 1/7")""",
    """(DTIME DN HCMC "7AM 4/7")""",
    """(ATIME DN DN "9AM 4/7")""",
    """(DTIME NT HCMC "7AM 1/7")""",
    """(ATIME NT NT "12AM 1/7")""",
    """(DTIME NT HCMC "7AM 5/7")""",
    """(ATIME NT NT "12AM 5/7")""",
    """(RUN-TIME PQ HCM PQ 2:00 HR)""",
    """(RUN-TIME DN HCM DN 2:00 HR)""",
    """(RUN-TIME NT HCM NT 5:00 HR)""",
    """(BY PQ airplane)""",
    """(BY DN airplane)""",
    """(BY NT train)"""
]

# Hàm phân loại cơ sở dữ liệu dựa trên loại thông tin
def categorize_database(database):
    arrival_times = [entry.replace('(', '').replace(')', '') for entry in database if 'ATIME' in entry]
    departure_times = [entry.replace('(', '').replace(')', '') for entry in database if 'DTIME' in entry]
    run_times = [entry.replace('(', '').replace(')', '') for entry in database if 'RUN-TIME' in entry]
    transportation_modes = [entry.replace('(', '').replace(')', '') for entry in database if 'BY' in entry]
    return {
        'arrival': arrival_times,
        'departure': departure_times,
        'runtime': run_times,
        'transportation': transportation_modes
    }

# Hàm chuyển đổi chuỗi dữ liệu thành từ điển để dễ dàng xử lý
def get_dict_for_tuple(data):
    parts = data.split(" ")
    if parts[0] in ["ATIME", "DTIME"]:
        return {
            'type': parts[0],
            'tourname': parts[1],
            'from': parts[2],
            'to': parts[1],  # Cùng địa điểm đến
            'time': f"{parts[3]} {parts[4]}"
        }
    if parts[0] == "RUN-TIME":
        return {
            'type': parts[0],
            'tourname': parts[1],
            'from': parts[2],
            'to': parts[3],
            'time': f"{parts[4]} {parts[5]}"
        }
    if parts[0] == "BY":
        return {
            'type': parts[0],
            'tourname': parts[1],
            'by': parts[2]
        }

# Hàm xử lý truy vấn và trả về kết quả
def retrieve_result(semantics):
    categorized_data = categorize_database(raw_database)
    result = ""
    question_type = 0

    if semantics["whtype"] == 'YESNO':
        if semantics["request"] == 'REMIND' and "tour" in semantics["gap"]:
            result += f"Có tổng cộng {len(categorized_data['departure'])} tour:\n"
            for departure in categorized_data['departure']:
                info = get_dict_for_tuple(departure)
                result += f"Tour đi từ {info['from']} đến {info['to']} khởi hành lúc {info['time']}\n"
            question_type = 1

    if semantics["whtype"] == 'HOWLONG':
        for runtime in categorized_data['runtime']:
            info = get_dict_for_tuple(runtime)
            if info["to"] == semantics["location"]:
                result += f"Tour đi từ {info['from']} đến {info['to']} mất {info['time']}"
        question_type = 2

    if semantics["whtype"] == 'HOWMANY':
        if "tour" in semantics["object"]:
            tour_count = sum(1 for arrival in categorized_data['arrival']
                             if get_dict_for_tuple(arrival)["to"] == semantics["location"])
            result += f"Có {tour_count} tour đi đến {semantics['location']}"
            question_type = 3
        if "date" in semantics["object"]:
            for arrival in categorized_data['arrival']:
                info = get_dict_for_tuple(arrival)
                if info["to"] == semantics["location"]:
                    date = info["time"].replace('"', '').split(" ")[1]
                    result += f"Đi {semantics['location']} có ngày {date}\n"
            question_type = 5

    if semantics["whtype"] == 'WHAT':
        tour_location = semantics["location"]
        for transport in categorized_data['transportation']:
            info = get_dict_for_tuple(transport)
            if info["tourname"] == semantics["location"]:
                result += f"Đi {tour_location} bằng {info['by']}\n"
        question_type = 4

    return result, question_type
