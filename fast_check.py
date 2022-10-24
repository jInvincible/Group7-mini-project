class Solution(object):
    def romanToInt(self, s):
        symbol_dic = {'I': 1, 'V': 5,
                      'X': 10, 'L': 50,
                      'C': 100, 'D': 500,
                      'M': 1000                     
                     }
        result = 0
        i = 0
        while i <= len(s):
            try:
                letter = s[i]
                right_letter = s[i+1]
                if symbol_dic[letter] >= symbol_dic[right_letter]:
                    result += symbol_dic[letter]
                    i+=1
                else:
                    result += symbol_dic[right_letter] - symbol_dic[letter]
                    i+=2
            except:
                if s[-1] == letter:
                        result += symbol_dic[s[-1]]
                return result
                    
roman_letter = Solution()
result = roman_letter.romanToInt('IV')
print(result)