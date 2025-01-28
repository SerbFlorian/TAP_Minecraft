from mcpi.minecraft import Minecraft

class MinecraftAmphitheater:
    def __init__(self, mc, start_x=92, start_y=72, start_z=556, base_width=40, base_length=60, height=20, num_levels=6):
        self.mc = mc  # Conexión al servidor de Minecraft
        self.start_x = start_x  # Coordenadas iniciales
        self.start_y = start_y
        self.start_z = start_z
        self.base_width = base_width  # Tamaño básico
        self.base_length = base_length
        self.height = height
        self.num_levels = num_levels
        # Materiales
        self.stone = 1  # Piedra
        self.stone_bricks = 98  # Ladrillos de piedra
        self.sandstone = 24  # Piedra arenisca para las paredes exteriores
        self.glass = 20  # Cristal para detalles

    def build_ellipse(self, center_x, center_y, center_z, width, length, block_type):
        """Genera una elipse (base ovalada)"""
        for x in range(center_x - width, center_x + width + 1):
            for z in range(center_z - length, center_z + length + 1):
                distance = ((x - center_x) ** 2) / (width ** 2) + ((z - center_z) ** 2) / (length ** 2)
                if distance <= 1:
                    self.mc.setBlock(x, center_y, z, block_type)

    def build_levels(self):
        """Construye los niveles escalonados del anfiteatro"""
        for i in range(self.num_levels):
            width = self.base_width - (i * 6)
            length = self.base_length - (i * 8)
            self.build_ellipse(self.start_x, self.start_y + i, self.start_z, width, length, self.stone_bricks)

    def build_walls(self):
        """Construye las paredes exteriores del anfiteatro"""
        for y in range(self.start_y, self.start_y + self.height):
            for x in range(self.start_x - self.base_width, self.start_x + self.base_width + 1):
                for z in range(self.start_z - self.base_length, self.start_z + self.base_length + 1):
                    distance = ((x - self.start_x) ** 2) / (self.base_width ** 2) + ((z - self.start_z) ** 2) / (self.base_length ** 2)
                    if distance > 1 and distance < 1.1:
                        self.mc.setBlock(x, y, z, self.sandstone)

    def build_entrances(self):
        """Crea las entradas principales del anfiteatro"""
        for z in range(self.start_z - 6, self.start_z + 6):
            for y in range(self.start_y, self.start_y + self.height):
                self.mc.setBlock(self.start_x - self.base_width - 1, y, z, self.sandstone)
                self.mc.setBlock(self.start_x + self.base_width + 1, y, z, self.sandstone)

    def build_roof(self):
        """Construye el techo del anfiteatro (opcional)"""
        for x in range(self.start_x - self.base_width, self.start_x + self.base_width + 1):
            for z in range(self.start_z - self.base_length, self.start_z + self.base_length + 1):
                self.mc.setBlock(x, self.start_y + self.num_levels, z, self.glass)

    def build_interior(self):
        """Construye los detalles internos del anfiteatro (arena y columnas)"""
        for x in range(self.start_x - self.base_width + 2, self.start_x + self.base_width - 2):
            for z in range(self.start_z - self.base_length + 2, self.start_z + self.base_length - 2):
                self.mc.setBlock(x, self.start_y, z, self.stone)
        for i in range(self.start_x - self.base_width + 5, self.start_x + self.base_width - 5, 10):
            for z in range(self.start_z - self.base_length + 5, self.start_z + self.base_length - 5, 10):
                self.mc.setBlock(i, self.start_y + 1, z, self.stone)

    def give_materials_to_player(self):
        """Añade materiales al inventario del jugador (solo mensaje)"""
        materials = [
            "piedra para la arena central",
            "ladrillos de piedra para las gradas",
            "piedra arenisca para las paredes exteriores",
            "cristal para el techo del anfiteatro"
        ]
        for material in materials:
            self.mc.postToChat(f"Se ha anadido al inventario del jugador el material: {material}.")

    def build_amphitheater(self):
        """Construir el anfiteatro completo"""
        self.build_levels()
        self.build_walls()
        self.build_entrances()
        self.build_roof()
        self.build_interior()
        self.give_materials_to_player()
        self.mc.postToChat("El Anfiteatro Romano de Tarragona ha sido generado exitosamente y los materiales han sido indicados!")


if __name__ == "__main__":
    mc = Minecraft.create()  # Conectar a Minecraft
    amphitheater = MinecraftAmphitheater(mc)
    amphitheater.build_amphitheater()  # Construir el anfiteatro
