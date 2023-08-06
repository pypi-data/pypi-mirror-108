import simpleapp
import simpleconfig
import simpleicons
import simplestyles
import simpleviews
import simplewidgets

app = simpleapp.App('test app', start_hidden=True)
main_view = simpleviews.SimpleView(app)

choices = []
for x in range(0, 9): choices.append(f'choice{x}')
dnd = simplewidgets.SimpleDragDropListbox(main_view, choices)

button = simplewidgets.SimpleButton(main_view, 'Execute', lambda: print(dnd.read_options()))

main_view.build_grid({
    'row1': dnd,
    'row2': button
    })

app.change_view(main_view)
app.start()