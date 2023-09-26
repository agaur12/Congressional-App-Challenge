from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label

class TestApp(App):
    def build(self):
        # Create a root layout (e.g., a BoxLayout)
        root_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Create widgets for testing
        label = Label(text='Hello, Kivy Test!')
        button = Button(text='Click Me')
        
        # Bind a function to the button press event
        button.bind(on_press=self.on_button_click)
        
        # Add widgets to the root layout
        root_layout.add_widget(label)
        root_layout.add_widget(button)
        
        return root_layout

    def on_button_click(self, instance):
        # Define what happens when the button is clicked
        self.root.ids.label.text = 'Button Clicked!'

if __name__ == '__main__':
    TestApp().run()
