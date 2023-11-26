class Vector2D:
    def __init__(self, x_component: float, y_component: float):

        self.vector: list = [x_component, y_component]
        self.x: float = x_component
        self.y: float = y_component

        # a^2+b^2=c^2, **0.5 = sqrt, represents magnitude or total distance
        self.magnitude: float = (self.x*self.x + self.y*self.y)**0.5

    def normalized(self):
        if self.magnitude == 0: return Vector2D(0, 0)
        return self / self.magnitude

    def __lt__(self, other):
        return self.magnitude < other

    def __gt__(self, other):
        return self.magnitude > other

    def __mul__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x * other.x, self.y * other.y)
        elif isinstance(other, float | int):
            return Vector2D(self.x * other, self.y * other)
        else:
            raise TypeError(f"Expected type: Vector2D or float, int, got {type(other)}")

    def __truediv__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x / other.x, self.y / other.y)
        elif isinstance(other, float | int):
            return Vector2D(self.x / other, self.y / other)
        else:
            raise TypeError(f"Expected type: Vector2D or float, int, got {type(other)}")

    def __add__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)
        elif isinstance(other, float | int):
            return Vector2D(self.x + other, self.y + other)
        else:
            raise TypeError(f"Expected type: Vector2D or float, int, got {type(other)}")

    def __sub__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x - other.x, self.y - other.y)
        elif isinstance(other, float | int):
            return Vector2D(self.x - other, self.y - other)
        else:
            raise TypeError(f"Expected type: Vector2D or float, int, got {type(other)}")

    def __rmul__(self, other): return self*other
    def __radd__(self, other): return self+other
    def __rsub__(self, other): return self-other

    def __getitem__(self, item):
        return self.vector[item]

    def __setitem__(self, key, value):
        self.vector[key] = value
        self.x, self.y = self.vector
        self.magnitude = (self.x*self.x + self.y*self.y)**0.5

    def __str__(self):
        return f'<{self.x}, {self.y}>'

    def __repr__(self): return str(self)

    def __abs__(self):
        return Vector2D(abs(self.x), abs(self.y))