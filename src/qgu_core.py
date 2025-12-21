import numpy as np

class QGU_Entity:
    """
    The fundamental unit of the QGU framework.
    Represents a discrete entity interacting via emergent rules.
    """
    def __init__(self, idx, pos, mass=1.0, fixed=False):
        self.id = idx
        self.pos = np.array(pos, dtype=float)
        self.vel = np.zeros(3)
        self.acc = np.zeros(3)
        self.mass = mass
        self.fixed = fixed
        self.local_density = 0.0
        self.time_dilation_factor = 1.0

    def update_state(self, dt=0.1):
        """Updates position based on velocity and computed time dilation."""
        if self.fixed: return
        
        # Apply Law-1: Effective dt depends on density
        # Time flows slower in high density
        effective_dt = dt * self.time_dilation_factor
        
        self.vel += self.acc * effective_dt
        self.pos += self.vel * effective_dt
        
        # Reset acceleration for next frame
        self.acc = np.zeros(3)

class QGU_System:
    """
    Manages the collection of QGU entities and physics interactions.
    """
    def __init__(self, num_particles=100, space_size=20):
        self.entities = []
        self.space_size = space_size
        self.g_const = 1.0
        
    def add_entity(self, pos, mass=1.0, fixed=False):
        idx = len(self.entities)
        entity = QGU_Entity(idx, pos, mass, fixed)
        self.entities.append(entity)
        return entity

    def calculate_gradient_acceleration(self, target_p, radius=5.0):
        """
        LAW 2 CORE: Calculates acceleration based on Density Gradient.
        Returns: Gradient Magnitude, Acceleration Magnitude
        """
        # 1. Measure Gradient (Change in Density)
        epsilon = 0.5
        grad = np.zeros(3)
        # We need a copy of pos to probe without moving the actual particle
        original_pos = target_p.pos.copy()
        
        # Temporary probe particle for density checks
        probe = QGU_Entity(-1, original_pos, 0, True)

        for axis in range(3):
            # Probe +ve direction
            probe.pos = original_pos.copy()
            probe.pos[axis] += epsilon
            d_plus = self._get_local_density(probe, radius)
            
            # Probe -ve direction
            probe.pos = original_pos.copy()
            probe.pos[axis] -= 2*epsilon
            d_minus = self._get_local_density(probe, radius)
            
            # Central Difference
            grad[axis] = (d_plus - d_minus) / (2 * epsilon)
            
        return np.linalg.norm(grad), np.linalg.norm(target_p.acc)

    def _get_local_density(self, target_p, radius):
        d = 0
        for p in self.entities:
            if p.id == target_p.id: continue
            dist = np.linalg.norm(p.pos - target_p.pos)
            if dist < radius:
                d += p.mass * (1 - dist/radius)
        return d
