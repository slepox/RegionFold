import sublime, sublime_plugin

def advance_to_first_non_white_space_on_line(view, pt):
    while True:
        c = view.substr(pt)
        if c == " " or c == "\t":
            pt += 1
        else:
            break

    return pt

class RegionFoldCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        def fold_region(r):
            #region Test Region
            view = self.view
            r_start = view.find("#region ", r.begin())
            if (r_start.a > r.end()):
                return r
            #endregion
            r_end = view.find("#endregion", r_start.b)
            if (r_end.a > r.end()):
                return r
            f_r = sublime.Region(view.line(r_start).a, view.line(r_end).b)
            view.fold(sublime.Region(advance_to_first_non_white_space_on_line(view, r_start.a)-1, r_start.b))
            view.fold(sublime.Region(view.line(r_start).b, f_r.b))
            return f_r
        
        # if self.view.sel()
        new_sel = []
        for s in self.view.sel():
            if not s.empty():
                new_sel.append(fold_region(s))
            # else:
                # if view.line(s).contains(view.find("#region", view.line(s).a)):
                #     fold_region()
        if len(new_sel) != 0:
            self.view.sel().clear()
            for r in new_sel:
                self.view.sel().add(r)
        else:
            fold_region(sublime.Region(0, self.view.size()))