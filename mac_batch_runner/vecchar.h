#ifndef VEC_CHAR_CLASS
#define VEC_CHAR_CLASS

template <class T>
class Vecchar
{
  private:
    T* arr;
    int size;
    int capacity;
    int minidx(int, int);
  public:
    Vecchar();
    Vecchar(T);
    ~Vecchar();
    void push(T);
    void push(const Vecchar<T>&);
    T get_element(int) const;
    T* get_array() const;
    T operator[] (int) const;
    void hard_reset();
    int get_size() const;
    int find(T*, int);
    Vecchar<T> subvec(int, int);
    bool equals(const Vecchar<T>&);
    bool equals(T*, int);
};

// PRIVATE FUNCTIONS

/**
 * Returns the minimum of the two numbers
 * @tparam T unused
 * @param idx1
 * @param idx2
 * @return minimum of two numbers
 */
template <class T>
int Vecchar<T>::minidx(int idx1, int idx2)
{
  if(idx1 > idx2)
    return idx2;
  return idx1;
}

// PUBLIC FUNCTIONS

/**
 * Starts off with a NULL array and size=0 capacity=0
 * @tparam T
 */
template <class T>
Vecchar<T>::Vecchar()
{
  size = 0;
  capacity = 0;
  arr = NULL;
}

/**
 * Starts off with 1 element for the Vecchar
 * @tparam T - should probably push('\0') for char arrays
 * @param element
 */
template <class T>
Vecchar<T>::Vecchar(T element)
{
  size = 1;
  capacity = 1;
  arr = new T[capacity];
  arr[0] = element;
}

template <class T>
Vecchar<T>::~Vecchar()
{
  delete[] arr;
}

/**
 * Pushes one element onto the Vecchar and resizes if size>=capacity
 * @tparam T - after last char pushed for char array, push '\0'
 * @param c element to push onto the array
 */
template <class T>
void Vecchar<T>::push(T c)
{
  if(size >= capacity)
  {
    capacity = (capacity == 0) ? 1 : capacity * 2;
    T* arr = new T[capacity];
    for(int i = 0; i < size; i++)
    {
      arr[i] = this->arr[i];
    }

    if(size > 0)
      delete[] this->arr;
    
    this->arr = arr;
  }

  this->arr[size] = c;
  size++;
}

template<class T>
void Vecchar<T>::push(const Vecchar<T>& vec)
{
  for(int i = 0; i < vec.get_size(); i++)
  {
    this->push(vec[i]);
  }
}

template <class T>
T Vecchar<T>::get_element(int idx) const
{
  return arr[idx];
}

template <class T>
T Vecchar<T>::operator[] (int idx) const
{
  return arr[idx];
}

template <class T>
T* Vecchar<T>::get_array() const
{
  return arr;
}

template <class T>
int Vecchar<T>::get_size() const
{
  return size;
}

/**
 * Checks if a smaller array is within the Vecchar's array.
 * @tparam T - Function acts the same for all types but char arrays (pass in
               SIZE-1 for size param when searching for char arrays unless
               Vecchar char array has '\0' at the end and is the same size as
               the sub array passed in)
 * @param subvec - smaller array we are checking if correct
 * @param size - size of the array - pass in size-1 for strings (DON'T INCLUDE
                 NULL CHAR)
 * @return -1 if arr not found, address if found (not -1)
 */
template <class T>
int Vecchar<T>::find(T* subarr, int size)
{
  // need to check if subarr will move past size of vector
  for(int i = 0; (i + size) < this->size; i++)
  {
    Vecchar<T>vec = this->subvec(i, size);
    if(vec.equals(subarr, size))
    {
      // return idx subarr was found
      return i;
    }
  }

  // arr was not found in this->arr
  return -1;
}

/**
 *
 * @tparam T
 * @param idx
 * @param len
 * @return
 */
template <class T>
Vecchar<T> Vecchar<T>::subvec(int idx, int len)
{
  Vecchar<T> vec;
  int last_idx;

  // never return past the end of the existing indicies
  last_idx = this->minidx((idx + len), (this->size));
  for(int i = idx; i < last_idx; i++)
  {
    vec.push(this->arr[i]);
  }

  return vec;
}

template <class T>
bool Vecchar<T>::equals(const Vecchar<T>& vec)
{
  if(vec.size != this->size)
    return false;

  if(vec.capacity != this->capacity)
    return false;

  for(int i = 0; i < this->size; i++)
  {
    if(vec[i] != this->get_element(i))
      return false;
  }

  return true;
}

template <class T>
bool Vecchar<T>::equals(T* arr, int size)
{
  if(size != this->size)
    return false;

  char c1 = '\0';
  char c2 = '\0';

  for(int i = 0; i < size; i++)
  {
    c1 = arr[i];
    c2 = this->get_element(i);
    if(c1 != c2)
      return false;
  }

  return true;
}

#endif //VEC_CHAR_CLASS