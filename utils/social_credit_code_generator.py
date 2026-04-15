import random
from utils import data

registration_departments = data.registration_departments

institution_types = data.institution_types

class SocialCreditCodeGenerator:
    def __init__(self):
        pass

    def generate_social_credit_code(self, district, registration_department=None, institution_type=None):
        try:
            dept_code = registration_department if registration_department else self.random_registration_department()
            institution_code = institution_type if institution_type else self.random_institutional_category(dept_code)
            county_code = district  # 使用传入的district参数
            organization_code = self.random_organization_code()
            social_code = dept_code + institution_code + county_code + organization_code
            check_code = self.calculate_check_code(social_code)
            social_code = social_code + check_code

            return social_code
        except Exception as e:
            print(f"Error generating social credit code: {e}")
            raise

    def validate_social_credit_code(self, social_code):
        try:
            if len(social_code) == 18:
                real_check_num = social_code[17]
                check_num = self.calculate_check_code(social_code[0:17])
                if check_num == real_check_num:
                    return '校验通过'
                else:
                    return '校验未通过'
            else:
                return '校验未通过，长度不为18位'
        except Exception as e:
            print(f"Error validating social credit code: {e}")
            return '校验失败'

    def random_registration_department(self):
        return random.choice(list(registration_departments.values()))

    def random_institutional_category(self, dept_code):
        return random.choice([item[0] for item in institution_types[dept_code]])

    def random_organization_code(self):
        try:
            weights = [3, 7, 9, 10, 5, 8, 4, 2]
            code_dict = {
                '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'J': 18, 'K': 19, 'L': 20, 'M': 21,
                'N': 22, 'P': 23, 'Q': 24, 'R': 25, 'T': 26, 'U': 27, 'W': 28, 'X': 29, 'Y': 30
            }
            total = 0
            organization_code = "".join(random.choice(list(code_dict.keys())) for _ in range(8))
            total = sum(code_dict[ci] * weights[i] for i, ci in enumerate(organization_code))

            check_num = 11 - (total % 11)
            if check_num == 10:
                check_num = 'X'
            elif check_num == 11:
                check_num = '0'
            else:
                check_num = str(check_num)

            return organization_code + check_num
        except Exception as e:
            print(f"Error generating organization code: {e}")
            raise

    def calculate_check_code(self, code):
        try:
            weights = [1, 3, 9, 27, 19, 26, 16, 17, 20, 29, 25, 13, 8, 24, 10, 30, 28]
            code_dict = {
                '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'J': 18, 'K': 19, 'L': 20, 'M': 21,
                'N': 22, 'P': 23, 'Q': 24, 'R': 25, 'T': 26, 'U': 27, 'W': 28, 'X': 29, 'Y': 30
            }
            total = 0
            for i, ci in enumerate(code):
                if ci in ['I', 'O', 'Z', 'S', 'V']:
                    return None
                total += code_dict[ci] * weights[i]

            pos = 31 - (total % 31)
            if pos == 31:
                pos = 0
            for k, v in code_dict.items():
                if v == pos:
                    return k
        except Exception as e:
            print(f"Error calculating check code: {e}")
            raise
