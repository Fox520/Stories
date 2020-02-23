from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.factory import Factory
from kivy.clock import Clock
from kivy.uix.image import AsyncImage
# v0.103.0
from kivymd.app import MDApp
from kivymd.uix.progressbar import ProgressBar

Builder.load_string('''
<ViewStatusScreen>:
    BoxLayout:
        orientation: "vertical"
        BoxLayout:
            id: box_progress_area
            size_hint_y: 0.1
            orientation: "horizontal"
        BoxLayout:
            id: image_view
            orientation: "vertical"

<-FullImage>:
    canvas:
        Color:
            rgb: (1, 1, 1)
        Rectangle:
            texture: self.texture
            size: self.width + 20, self.height + 20
            pos: self.x - 10, self.y - 10

''')


# Copy pasta https://kivy.org/doc/stable/api-kivy.uix.image.html#alignment
class FullImage(AsyncImage):
    pass


class ViewStatusScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box_progress_area = self.ids["box_progress_area"]
        self.image_view = self.ids["image_view"]
        self.current_image = None
        self.initial_viewing = True
        self.current_pb = None
        self.total_time = 0
        # Length of time before switching to next image in queue
        self.MAX_TIME = 10

    def on_enter(self):
        self.image_queue = []
        # Sample images
        self.image_queue.append(Factory.FullImage(source="https://images.unsplash.com/photo-1525609004556-c46c7d6cf023?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=389&q=80", allow_stretch=False))
        self.image_queue.append(Factory.FullImage(source="https://imgd.aeplcdn.com/1056x594/cw/ec/37710/Maruti-Suzuki-Baleno-Right-Front-Three-Quarter-147420.jpg", allow_stretch=False))
        self.image_queue.append(Factory.FullImage(source="https://image.shutterstock.com/image-vector/education-flat-icon-set-flyer-600w-397626016.jpg", allow_stretch=False))
        
        self.progress_bars_list = []
        # Add the progress bars to queue for tracking
        for _ in range(len(self.image_queue)):
            self.progress_bars_list.append(ProgressBar(max=1, value=0))
        
        # Now add them to screen
        for i in self.progress_bars_list:
            self.box_progress_area.add_widget(i)
        # Periodically 
        Clock.schedule_interval(self.show_status_images, 1)
    
    # This is where the magic happens
    def show_status_images(self, dt):
        try:
            if self.total_time >= self.MAX_TIME:
                # Load up new image
                self.current_pb = self.progress_bars_list.pop(0)
                # Remove old image from screen
                self.image_view.remove_widget(self.current_image)
                # Get the new image from list and display it
                self.current_image = self.image_queue.pop(0)
                self.image_view.add_widget(self.current_image)
                # Reset timer
                self.total_time = 0
            elif self.total_time < self.MAX_TIME:
                # Get a progress bar if there isn't one available already
                if self.current_pb is None: self.current_pb = self.progress_bars_list.pop(0)
                if self.current_pb.value < 1:
                    try:
                        if self.initial_viewing:
                            self.current_image = self.image_queue.pop(0)
                            self.image_view.add_widget(self.current_image)
                            self.initial_viewing = False
                        # Increment progress bar value
                        self.current_pb.value += 0.1
                    except IndexError:
                        print("no images left to show")
                        # Reset current progress bar
                        self.current_pb = None
            # Increment timer
            self.total_time += dt
                
        except IndexError:
            print("no progress bars left, show status of next user")
        

        


class Twizzer(MDApp):
    def build(self):
        self.title = "Twizzer"
        self.sm = ScreenManager()
        self.sm.add_widget(ViewStatusScreen(name="sample"))
        return self.sm

Twizzer().run()