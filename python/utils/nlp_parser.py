def extract_location(entities_list):
    """
    Tìm và trả về địa điểm đầu tiên trong danh sách `entities_list` phù hợp với các mã địa điểm cụ thể (NT, DN, HCM, PQ).
    Đồng thời loại bỏ địa điểm này khỏi danh sách.

    Args:
        entities_list (list): Danh sách các thực thể chứa tên hoặc mã địa điểm.

    Returns:
        tuple: (Địa điểm được tìm thấy, danh sách còn lại sau khi loại bỏ địa điểm đó).
    """
    result = None
    for location in entities_list:
        if 'NT' in location or 'DN' in location or 'HCM' in location or 'PQ' in location:
            entities_list.remove(location)
            result = location        
    return result, entities_list 

def find_name_containing(entities_list, keyword):
    """
    Tìm tên của thực thể trong danh sách có chứa một từ khóa cụ thể.

    Args:
        entities_list (list): Danh sách các thực thể (có thuộc tính `name`).
        keyword (str): Từ khóa cần tìm.

    Returns:
        str: Tên của thực thể chứa từ khóa hoặc chuỗi rỗng nếu không tìm thấy.
    """
    result = ''
    for x in entities_list:
        if keyword in x.name:
            result = x.name
    return result
    

def parse_to_procedure(logical_tree):   
    """
    Phân tích cây logic để tạo ra các tham số cần thiết cho thủ tục xử lý.

    Args:
        logical_tree: Cây logic được sinh ra từ trình phân tích cú pháp.

    Returns:
        dict: Tham số được phân tích, bao gồm loại câu hỏi (`whtype`) và các chi tiết liên quan.
    """
    logical_expression = logical_tree.label()['SEM']
    
    result = {}
    
    whquery = list(logical_expression.args)[-1]
    whqParas = [pred.name for pred in whquery.constants()]
    if 'YESNO' in whqParas:
        whtype = 'YESNO'
        request_expression = list(logical_expression.args)[0]
        request = list(request_expression.predicates())[0].name
        gap = find_name_containing(request_expression.constants(), 'tour')
        result = {'whtype': whtype, 'request': request, 'gap': gap}
        
    if 'HOWLONG' in whqParas:
        whtype = 'HOWLONG'
        request_expression = list(logical_expression.args)[0]
        entities_list = [pred.name for pred in request_expression.constants()]
        location, objects = extract_location(entities_list)
        result = {'whtype': whtype, 'location': location}
        
    if 'HOWMANY' in whqParas:
        whtype = 'HOWMANY'
        request_expression = list(logical_expression.args)[0]
        entities_list = [pred.name for pred in request_expression.constants()]
        location, objects = extract_location(entities_list)
        result = {'whtype': whtype, 'location': location, 'object': objects[0]}

    if 'WHAT' in whqParas:
        whtype = 'WHAT'
        request_expression = list(logical_expression.args)[0]
        entities_list = [pred.name for pred in request_expression.constants()]
        location, objects = extract_location(entities_list)
        result = {'whtype': whtype, 'location': location, 'object': objects[0]}
    
    return result
    