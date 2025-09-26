
from manim import *

class EinsteinEquation(Scene):
    def construct(self):
        # Set black background
        self.camera.background_color = BLACK
        
        # Create the equation parts
        E = MathTex("E", color=YELLOW, font_size=120)
        equals = MathTex("=", color=YELLOW, font_size=120)
        m = MathTex("m", color=YELLOW, font_size=120)
        c = MathTex("c", color=YELLOW, font_size=120)
        squared = MathTex("^2", color=YELLOW, font_size=120)
        
        # Position the parts to form the complete equation
        equation_group = VGroup(E, equals, m, c, squared)
        equation_group.arrange(RIGHT, buff=0.2)
        equation_group.move_to(ORIGIN)
        
        # Create the subtitle
        subtitle = Text("Einstein's Mass-Energy Equivalence", 
                       color=WHITE, font_size=24)
        subtitle.next_to(equation_group, DOWN, buff=0.8)
        
        # Animate each part appearing with writing effect
        self.play(Write(E), run_time=0.3)
        self.wait(0.1)
        
        self.play(Write(equals), run_time=0.3)
        self.wait(0.1)
        
        self.play(Write(m), run_time=0.3)
        self.wait(0.1)
        
        self.play(Write(c), run_time=0.3)
        self.wait(0.1)
        
        self.play(Write(squared), run_time=0.3)
        self.wait(0.3)
        
        # Add the subtitle
        self.play(Write(subtitle), run_time=0.4)
        self.wait(0.2)
        
        # Create glowing effect
        glow_equation = equation_group.copy()
        glow_equation.set_stroke(YELLOW, width=8, opacity=0.7)
        
        # Animate the glow effect
        self.add(glow_equation)
        self.play(
            glow_equation.animate.set_stroke(opacity=0),
            run_time=0.6
        )
        self.remove(glow_equation)
        
        self.wait(0.3)
