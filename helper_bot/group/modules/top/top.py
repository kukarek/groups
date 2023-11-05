from .executor import Executor


class Top(Executor):

    def Get_top(self, group_id):
        
        top = 0
        file_path = 'helper_bot/group/modules/top/executor/html_page.html'  # Имя файла, куда будет сохранена HTML страница
    
        self.download_html(file_path)
        html = self.read_html(file_path)
        cleaned_html = self.remove_before_first_group(html)
        group_strings = self.extract_group_strings(cleaned_html)
        a = len(group_strings)
        for i in range(a):
                            
            if group_strings[i].find(group_id) != -1:
                top = i+1

        if(top == 0):
            return 40
        else:
            return top