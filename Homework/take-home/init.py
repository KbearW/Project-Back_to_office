
class Canvas():
    """Canvas class to render canvas with a specified height and width"""
    def __init__(self,height,width):
        self.elements = []
        self.height=height
        self.width=width
    
class Shape():
    """Shape class render the shape based on input"""
    
class Rectangle(Shape):
    """A rectangle. """
    def __init__(self, start_x: int, start_y: int, end_x: int, end_y: int, fill_char: str):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.fill_char = fill_char

        

# def canvas():
#     height = int(input('height (int only): '))
#     width = int(input('width (int only): '))
#     create_canvas={'height':height, 'width':width}

# def print_reg():
#     rows = int(input('height (int only): '))
#     cols = int(input('width (int only): '))
#     char = input('Please enter a character :')

#     for i in range(rows):
#         for j in range(cols):
#             print(char, end = ' ')
#         print()

# print_reg()
# answer = input('Would you like to print another? [y/n]')
# if answer =='y':
#     print_reg()
# else:
#     print('goodbye')
