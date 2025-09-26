from manim import *

class DerivativeAnimation(Scene):
    def construct(self):
        # Create coordinate system
        axes = Axes(
            x_range=[-0.5, 4.5, 1],
            y_range=[-1, 16, 2],
            x_length=7,
            y_length=5,
            axis_config={"color": BLUE}
        )
        
        # Function f(x) = x^2
        curve = axes.plot(lambda x: x**2, color=YELLOW, x_range=[0, 4])
        
        # Title
        title = Text("Calculus: Visualizing the Derivative", font_size=32).to_edge(UP)
        
        # Points P and Q
        x_p, y_p = 2, 4  # f(2) = 4
        x_q_start, y_q_start = 4, 16  # f(4) = 16
        
        point_p = Dot(axes.c2p(x_p, y_p), color=RED)
        point_q = Dot(axes.c2p(x_q_start, y_q_start), color=GREEN)
        
        label_p = Text("P", font_size=20, color=RED).next_to(point_p, DOWN+LEFT)
        label_q = Text("Q", font_size=20, color=GREEN).next_to(point_q, UP+RIGHT)
        
        # Initial secant line
        secant_line = Line(
            axes.c2p(x_p, y_p),
            axes.c2p(x_q_start, y_q_start),
            color=WHITE
        )
        
        # Slope formula
        slope_text = MathTex(r"\text{Slope} = \frac{\Delta y}{\Delta x}", font_size=24)
        slope_text.to_corner(UL)
        
        # Initial slope calculation
        initial_slope = (y_q_start - y_p) / (x_q_start - x_p)
        slope_calc = MathTex(f"= \\frac{{16-4}}{{4-2}} = 6", font_size=20)
        slope_calc.next_to(slope_text, DOWN, aligned_edge=LEFT)
        
        # Set up scene
        self.add(title)
        self.play(Create(axes))
        self.play(Create(curve))
        self.play(Create(point_p), Write(label_p))
        self.play(Create(point_q), Write(label_q))
        self.play(Create(secant_line))
        self.play(Write(slope_text), Write(slope_calc))
        
        self.wait(1)
        
        # Animate Q moving toward P
        x_values = [3.5, 3.0, 2.8, 2.5, 2.3, 2.1, 2.05]
        
        for x_q in x_values:
            y_q = x_q**2
            slope = (y_q - y_p) / (x_q - x_p)
            
            new_point_q = Dot(axes.c2p(x_q, y_q), color=GREEN)
            new_label_q = Text("Q", font_size=20, color=GREEN).next_to(new_point_q, UP+RIGHT)
            new_secant = Line(axes.c2p(x_p, y_p), axes.c2p(x_q, y_q), color=WHITE)
            new_calc = MathTex(f"= {slope:.1f}", font_size=20).next_to(slope_text, DOWN, aligned_edge=LEFT)
            
            self.play(
                Transform(point_q, new_point_q),
                Transform(label_q, new_label_q),
                Transform(secant_line, new_secant),
                Transform(slope_calc, new_calc),
                run_time=0.4
            )
        
        # Transform to derivative
        derivative_text = MathTex(r"\frac{dy}{dx} = 2x", font_size=24).to_corner(UL)
        at_point = MathTex(r"\text{At } x=2: \frac{dy}{dx} = 4", font_size=20)
        at_point.next_to(derivative_text, DOWN, aligned_edge=LEFT)
        
        # Tangent line (slope = 4 at x=2)
        tangent_line = Line(
            axes.c2p(1.5, 1),
            axes.c2p(2.5, 7),
            color=ORANGE
        )
        
        self.play(
            FadeOut(point_q),
            FadeOut(label_q),
            Transform(slope_text, derivative_text),
            Transform(slope_calc, at_point),
            Transform(secant_line, tangent_line)
        )
        
        # Add final labels
        tangent_label = Text("Tangent Line", font_size=18, color=ORANGE)
        tangent_label.next_to(tangent_line, RIGHT)
        self.play(Write(tangent_label))
        
        self.wait(3)
