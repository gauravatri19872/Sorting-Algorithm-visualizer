import tkinter as tk
import random
from PIL import Image, ImageTk
import time
import colorsys

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Visualizer")
        self.root.geometry("800x600")

        # Canvas to draw the bars representing the array
        self.canvas = tk.Canvas(root, width=800, height=400, bg="white")
        self.canvas.pack(pady=20)

        # Frame to hold various UI elements
        self.frame = tk.Frame(root)
        self.frame.pack(side=tk.BOTTOM)

        # Buttons for selecting sorting algorithms
        self.algorithms = ["Bubble Sort", "Insertion Sort", "Selection Sort", "Merge Sort", "Quick Sort", "Heap Sort"]
        self.algorithm_buttons = []
        for algorithm in self.algorithms:
            button = tk.Button(self.frame, text=algorithm, command=lambda alg=algorithm: self.set_algorithm(alg))
            button.pack(side=tk.LEFT, padx=5)
            self.algorithm_buttons.append(button)

        # Label and Entry for inputting array size
        tk.Label(self.frame, text="Array Size:").pack(side=tk.LEFT, padx=10)
        self.size_var = tk.IntVar()
        self.size_var.set(50)
        self.size_entry = tk.Entry(self.frame, textvariable=self.size_var, width=8)
        self.size_entry.pack(side=tk.LEFT, padx=10)

        # Label and Entry widgets for lower and upper limits of array values
        tk.Label(self.frame, text="Lower Limit:").pack(side=tk.LEFT, padx=10)
        self.lower_limit_var = tk.IntVar()
        self.lower_limit_var.set(10)
        self.lower_limit_entry = tk.Entry(self.frame, textvariable=self.lower_limit_var, width=8)
        self.lower_limit_entry.pack(side=tk.LEFT, padx=10)

        tk.Label(self.frame, text="Upper Limit:").pack(side=tk.LEFT, padx=10)
        self.upper_limit_var = tk.IntVar()
        self.upper_limit_var.set(400)
        self.upper_limit_entry = tk.Entry(self.frame, textvariable=self.upper_limit_var, width=8)
        self.upper_limit_entry.pack(side=tk.LEFT, padx=10)

        # Slider for selecting sorting speed
        tk.Label(self.frame, text="Speed:").pack(side=tk.LEFT, padx=10)
        self.speed_var = tk.DoubleVar()
        self.speed_var.set(1.0)
        self.speed_scale = tk.Scale(self.frame, from_=0.1, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, label="Speed", variable=self.speed_var)
        self.speed_scale.pack(side=tk.LEFT, padx=10)

        # Buttons to start sorting and reset the array
        self.sort_button = tk.Button(self.frame, text="Sort", command=self.sort)
        self.sort_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(self.frame, text="Reset", command=self.reset)
        self.reset_button.pack(side=tk.LEFT, padx=10)

        # Initialize array and draw it
        self.array = []
        self.reset()

    def reset(self):
        # Generate a random array within the specified limits
        array_size = self.size_var.get()
        self.array = [random.randint(self.lower_limit_var.get(), self.upper_limit_var.get()) for _ in range(array_size)]
        self.draw_array()

    def draw_array(self, colors=None):
        # Clear the canvas and draw bars based on the array values
        self.canvas.delete("all")
        bar_width = 800 / len(self.array)

        for i, height in enumerate(self.array):
            x1 = i * bar_width
            y1 = 400 - height
            x2 = (i + 1) * bar_width
            y2 = 400

            # Generate a color based on the height of the bar
            if colors is None:
                hue = height / 400.0  # Normalize height to be between 0 and 1
                rgb = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 1.0, 1.0)]
                color = "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])
            else:
                color = colors[i]

            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

        self.root.update_idletasks()

    def set_algorithm(self, algorithm):
        # Update the current algorithm to the selected one
        self.current_algorithm = algorithm

    def sort(self):
        # Determine which sorting algorithm to use based on the selected option
        if hasattr(self, 'current_algorithm'):
            if self.current_algorithm == "Bubble Sort":
                self.bubble_sort()
            elif self.current_algorithm == "Insertion Sort":
                self.insertion_sort()
            elif self.current_algorithm == "Selection Sort":
                self.selection_sort()
            elif self.current_algorithm == "Merge Sort":
                self.merge_sort()
            elif self.current_algorithm == "Quick Sort":
                self.quick_sort()
            elif self.current_algorithm == "Heap Sort":
                self.heap_sort()

    def delay(self):
        # Introduce a delay to control the sorting speed
        time.sleep(self.speed_var.get())

    def bubble_sort(self):
        # Bubble sort algorithm
        n = len(self.array)
        for i in range(n - 1):
            for j in range(0, n - i - 1):
                if self.array[j] > self.array[j + 1]:
                    self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]
                    self.draw_array()
                    self.delay()

    def insertion_sort(self):
        # Insertion sort algorithm
        for i in range(1, len(self.array)):
            key = self.array[i]
            j = i - 1
            while j >= 0 and key < self.array[j]:
                self.array[j + 1] = self.array[j]
                j -= 1
            self.array[j + 1] = key
            self.draw_array()
            self.delay()

    def selection_sort(self):
        # Selection sort algorithm
        for i in range(len(self.array)):
            min_index = i
            for j in range(i + 1, len(self.array)):
                if self.array[j] < self.array[min_index]:
                    min_index = j
            self.array[i], self.array[min_index] = self.array[min_index], self.array[i]
            self.draw_array()
            self.delay()

    def merge_sort(self):
        # Merge sort algorithm
        def merge(arr, left, mid, right):
            n1 = mid - left + 1
            n2 = right - mid

            left_arr = [0] * n1
            right_arr = [0] * n2

            for i in range(n1):
                left_arr[i] = arr[left + i]

            for j in range(n2):
                right_arr[j] = arr[mid + 1 + j]

            i = j = 0
            k = left

            while i < n1 and j < n2:
                if left_arr[i] <= right_arr[j]:
                    arr[k] = left_arr[i]
                    i += 1
                else:
                    arr[k] = right_arr[j]
                    j += 1
                k += 1

            while i < n1:
                arr[k] = left_arr[i]
                i += 1
                k += 1

            while j < n2:
                arr[k] = right_arr[j]
                j += 1
                k += 1

        def merge_sort_helper(arr, left, right):
            if left < right:
                mid = (left + right) // 2

                merge_sort_helper(arr, left, mid)
                merge_sort_helper(arr, mid + 1, right)

                merge(arr, left, mid, right)
                self.draw_array()
                self.delay()

        merge_sort_helper(self.array, 0, len(self.array) - 1)

    def quick_sort(self):
        # Quick sort algorithm
        def partition(arr, low, high):
            pivot = arr[high]
            i = low - 1
            for j in range(low, high):
                if arr[j] < pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            return i + 1

        def quick_sort_helper(arr, low, high):
            if low < high:
                pi = partition(arr, low, high)
                quick_sort_helper(arr, low, pi - 1)
                quick_sort_helper(arr, pi + 1, high)
                self.draw_array()
                self.delay()

        quick_sort_helper(self.array, 0, len(self.array) - 1)

    def heap_sort(self):
        # Heap sort algorithm
        def heapify(arr, n, i):
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2

            if left < n and arr[i] < arr[left]:
                largest = left

            if right < n and arr[largest] < arr[right]:
                largest = right

            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]
                heapify(arr, n, largest)

        n = len(self.array)

        for i in range(n // 2 - 1, -1, -1):
            heapify(self.array, n, i)

        for i in range(n - 1, 0, -1):
            self.array[i], self.array[0] = self.array[0], self.array[i]
            heapify(self.array, i, 0)
            self.draw_array()
            self.delay()

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()