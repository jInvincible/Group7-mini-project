'''Write a function to find the longest common prefix string amongst an array of strings.

If there is no common prefix, return an empty string "".

 

Example 1:

Input: strs = ["flower","flow","flight"]
Output: "fl"
Example 2:

Input: strs = ["dog","racecar","car"]
Output: ""
Explanation: There is no common prefix among the input strings.
 

Constraints:

1 <= strs.length <= 200
0 <= strs[i].length <= 200
strs[i] consists of only lowercase English letters.
'''
class Solution(object):
    def longestCommonPrefix(self, strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        result = ''        
        indexes = [len(i) for i in strs]
        indexes.sort()
        min_index = indexes[0]
        for i in range(min_index):
            for a in range(len(strs)):
                check = strs[a][i]
                if strs[a] != strs[-1]:
                    if strs[a][i] == strs[a+1][i]:
                        check = strs[a][i]
                    else:
                        check = ''
                        break
            result += check
        return result

# Fastest solution
# class Solution(object):
#     def longestCommonPrefix(self, strs):
#         """
#         :type strs: List[str]
#         :rtype: str
#         """
#         ans = ''
#         for i in range(len(strs[0])):
#             for j in strs:
#                 if len(j) < i+1 or strs[0][i] != j[i]:
#                        return ans
#             ans += strs[0][i]
#         return ans