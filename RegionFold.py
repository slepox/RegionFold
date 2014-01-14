import sublime, sublime_plugin

def fold_top_region(view, r):
    ##region Test Region
    r_start = view.find("#region", r.begin())
    if (r_start.a > r.end()):
        return r
    ##endregion
    r_end = view.find("#endregion", r_start.b)
    if (r_end.a > r.end()):
        return r
    f_r = sublime.Region(view.line(r_start).a, view.line(r_end).b)
    view.fold(sublime.Region(view.word(r_start).a, r_start.b))
    view.fold(sublime.Region(view.line(r_start).b, f_r.b))
    return f_r

class RegionFoldCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if len(self.view.sel()) != 0:
            new_sel = []
            for s in self.view.sel():
                if not s.empty():
                    new_sel.append(fold_top_region(self.view, s))
            self.view.sel().clear()
            for r in new_sel:
                self.view.sel().add(r)
        else:
            fold_top_region(self.view, sublime.Region(0, self.view.size()))