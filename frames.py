''' Compute deformation in different Earth reference frames '''
import math
import listmath as lm

class ref_frame_relative_to_CE:
    ''' Degree one load love numbers (Eulerian r.f.) '''
    alpha = float('nan')
    # Farell's LLN for CE
    _h = -0.290
    _l = 0.113
    _k = 0.0
    @property
    def h(self):
        return self._h - self.alpha
    @property
    def l(self):
        return self._l - self.alpha
    @property
    def k(self):
        return self._k - self.alpha

class CE(ref_frame_relative_to_CE): 
    ''' Center of solid Earth '''
    alpha = 0.0

class CM(ref_frame_relative_to_CE): 
    ''' Center of entire Earth '''
    alpha = 1.0

class CF(ref_frame_relative_to_CE): 
    ''' Center of surface Figure '''
    alpha = -0.021

class CL(ref_frame_relative_to_CE): 
    ''' Center of lateral surface Figure '''
    alpha = 0.113

class CH(ref_frame_relative_to_CE): 
    ''' Center of height surface Figure '''
    alpha = -0.290

def rp_to_xy(r, p):
    x = lm.mul(lm.cos(p), r)
    y = lm.mul(lm.sin(p), r)
    return x, y

def xy_to_rp(x, y):
    r = lm.sqrt(lm.add(lm.square(x), lm.square(y)))
    p = lm.atan2(y, x)
    return r,  p

def moment_hl_from_rp(r, p):
    mh = lm.sin(p) 
    ml = lm.cos(p)
    return mh, ml

def xy_from_xy_to_hl(x, y, xpos, ypos):
    rpos, ppos = xy_to_rp(xpos, ypos)
    h = lm.add(lm.mul(x, lm.cos(ppos)), lm.mul(y, lm.sin(ppos)))
    l = lm.sub(lm.mul(y, lm.cos(ppos)), lm.mul(x, lm.sin(ppos)))
    return h, l

def hl_from_xy_to_xy(h, l, xpos, ypos):
    rpos, ppos = xy_to_rp(xpos, ypos)
    x = lm.sub(lm.mul(h, lm.cos(ppos)), lm.mul(l, lm.sin(ppos)))
    y = lm.add(lm.mul(l, lm.cos(ppos)), lm.mul(h, lm.sin(ppos)))
    return x, y

if __name__ == '__main__':
    # Set up observation points on circle
    # around origin, simulating earth
    radius = 5.
    r = [radius            for _ in range(0,    360, 10)]
    p = [math.pi * p / 180 for p in range(-180, 180, 10)]
    
    # Duplicate the first point on the end
    # to `close` the circle
    r.append(r[0])
    p.append(p[0])
    
    # Test coordinate transformations from 
    # cartesian to polar
    x, y   = rp_to_xy(r, p)
    r2, p2 = xy_to_rp(x, y)
    assert all(lm.close(r, r2))
    assert all(lm.close(p, p2))

    # Compute axially aligned moment load
    mh, ml = moment_hl_from_rp(r, p)

    # Test hl to xy basis transformation
    mx, my = hl_from_xy_to_xy(mh, ml, x, y)
    mx_expect = [0. for _ in range(len(mh))]
    my_expect = [1. for _ in range(len(ml))]
    assert all(lm.close(mx, mx_expect))
    assert all(lm.close(my, my_expect))

    # Test xy to hl basis transformation
    mh2, ml2 = xy_from_xy_to_hl(mx, my, x, y)
    assert all(lm.close(mh, mh2))
    assert all(lm.close(ml, ml2))

    # Reference frames and output paths
    # to write observation positions and
    # perturbations in the respective frame
    ref_frames = [CE(), CM(), CF(), CH(), CL()]
    paths = [f"observation_{r}.dat" for r in ["ce", "cm", "cf", "ch", "cl"]]

    record_length = len(x)
    for ref, path in zip(ref_frames, paths):

        # Transform perturbation in CE reference frame
        # to the `ref` reference frame
        delsh = lm.scale(mh, ref.h)
        delsl = lm.scale(ml, ref.l)
    
        # Coordinate transformation from hl basis to xy basis
        dx, dy = hl_from_xy_to_xy(delsh, delsl, x, y)

        # Compute deformed observation points
        # x2 = lm.add(dx, x)
        # y2 = lm.add(dy, y)
    
        # Record observation position and perturbation in xy basis
        with open(path, "w") as file:
            for count, (_x, _y, _dx, _dy) in enumerate(zip(x, y, dx, dy)):
                file.write(f"{_x:.7f} {_y:.7f} {_dx:.7f} {_dy:.7f}")
                file.write("\n" if count + 1 != record_length else "")
