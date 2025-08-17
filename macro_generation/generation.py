import gdstk
import random
import math
length = 4  # Reduced from 8
avg_width = 1  # Reduced from 3
gap = 1  # Reduced from 1

min_metal6_width = 1.64  # Minimum Metal6 width in microns
min_metal6_spacing = 1.64 

# The GDSII file is called a library, which contains multiple cells.
lib = gdstk.Library()

# Geometry must be placed in cells.
cell = lib.new_cell("my_logo")

# Increase the grid size to create more TopMetal1 coverage
for i in range(1):  # Reduced from 10
    for j in range(1):  # Reduced from 10

        horz_width = math.sin(i*math.pi/3)*avg_width + 2
        vert_width = math.sin(j*math.pi/7)*avg_width + 2
        
        if random.random() > 0.5:
            rotdir = -1
        else:
            rotdir = 1

        # Create the geometry (a single rectangle) and add it to the cell.
        tx = j*(length)
        ty = i*(length)
        
        outerrect = gdstk.rectangle((tx, ty), (tx+length, ty+length), layer=12)  # Metal5
        
        if rotdir > 0:
            #low_rect = gdstk.rectangle((tx+(length-horz_width)/2, ty), (tx+(length-horz_width)/2+horz_width, ty+length), layer=126)  # TopMetal1
            rect = gdstk.rectangle((tx, ty+(length-vert_width)/2), (tx+length, ty+(length-vert_width)/2+vert_width), layer=12)  # Metal5

            #stub = (length-vert_width-gap*2)/2
            #rectLeft = gdstk.rectangle((tx+(length-horz_width)/2, ty), (tx+(length-horz_width)/2+horz_width, ty+stub), layer=126)  # TopMetal1
            #rectRight = gdstk.rectangle((tx+(length-horz_width)/2, ty+length-stub), (tx+(length-horz_width)/2+horz_width, ty+length), layer=126)  # TopMetal1
        else:
            #low_rect = gdstk.rectangle((tx, ty+(length-vert_width)/2), (tx+length, ty+(length-vert_width)/2+vert_width), layer=126)  # TopMetal1
            rect = gdstk.rectangle((tx+(length-horz_width)/2, ty), (tx+(length-horz_width)/2+horz_width, ty+length), layer=12)  # Metal5

            #stub = (length-horz_width-gap*2)/2
            #rectLeft = gdstk.rectangle((tx, ty+(length-vert_width)/2), (tx+stub, ty+(length-vert_width)/2+vert_width), layer=126)  # TopMetal1
            #rectRight = gdstk.rectangle((tx+length-stub, ty+(length-vert_width)/2), (tx+length, ty+(length-vert_width)/2+vert_width), layer=126)  # TopMetal1

            
        
        if random.random() > 0:
            rect.rotate(-math.pi/2, (tx+length/2, ty+length/2))
            #low_rect.rotate(-math.pi/2, (tx+length/2, ty+length/2))
            #rectLeft.rotate(-math.pi/2, (tx+length/2, ty+length/2))
            #rectRight.rotate(-math.pi/2, (tx+length/2, ty+length/2))
        
            
        
        #cell.add(outerrect)
        #cell.add(low_rect)
        cell.add(rect)
        #cell.add(rectLeft)
        #cell.add(rectRight)

# Add PR boundary (placement and routing boundary)
# Layer 189, datatype 4 for IHP SG13G2 PR boundary
pr_boundary = gdstk.rectangle((0, 0), (32, 32), layer=189, datatype=4)
cell.add(pr_boundary)


# Generate LEF file
def write_lef_file(filename, cell_name, cell_bounds, pins):
    """Write a LEF file for the cell"""
    with open(filename, 'w') as f:
        f.write("# LEF file generated for {}\n".format(cell_name))
        f.write("VERSION 5.8 ;\n")
        f.write("NAMESCASESENSITIVE ON ;\n")
        f.write("DIVIDERCHAR \"/\" ;\n")
        f.write("BUSBITCHARS \"[]\" ;\n")
        f.write("UNITS\n")
        f.write("   DATABASE MICRONS 1000 ;\n")
        f.write("END UNITS\n\n")
        
        # Define the cell
        f.write("MACRO {}\n".format(cell_name))
        f.write("   CLASS BLOCK ;\n")
        f.write("   FOREIGN {} 0 0 ;\n".format(cell_name))
        f.write("   SIZE {:.3f} BY {:.3f} ;\n".format(cell_bounds[2] - cell_bounds[0], cell_bounds[3] - cell_bounds[1]))
        f.write("   SYMMETRY X Y ;\n")
        
        # No pins - pure blackbox module
        
        # Add routing obstructions
        f.write("   OBS\n")
        f.write("      LAYER Metal1 ;\n")
        f.write("      RECT {:.3f} {:.3f} {:.3f} {:.3f} ;\n".format(
            cell_bounds[0], cell_bounds[1], cell_bounds[2], cell_bounds[3]))
        f.write("   END\n")
        
        f.write("END {}\n".format(cell_name))

# Calculate cell bounds (back to original size)
cell_width = 32  # 32 microns
cell_height = 32  # 32 microns
cell_bounds = (0, 0, cell_width, cell_height)

# Write LEF file
write_lef_file("../macros/my_logo.lef", "my_logo", cell_bounds, [])

# Save the library in a GDSII or OASIS file.
lib.write_gds("../macros/my_logo.gds")

# Optionally, save an image of the cell as SVG.
cell.write_svg("../macros/my_logo.svg")