#ifndef VEC_CHAR_CLASS
#define VEC_CHAR_CLASS

template <class T>
class Vecchar
{
  private:
    T* arr;
    int size;
    int capacity;
  public:
    Vecchar();
    Vecchar(T);
    ~Vecchar();
    void push(T c);
    T get_element(int);
    T* get_array();
    T operator[] (int);
    void hard_reset();
    int get_size();
};

template <class T>
Vecchar<T>::Vecchar()
{
  size = 0;
  capacity = 0;
  arr = NULL;
}

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

template <class T>
T Vecchar<T>::get_element(int idx)
{
  return arr[idx];
}

template <class T>
T Vecchar<T>::operator[] (int idx)
{
  return arr[idx];
}

template <class T>
T* Vecchar<T>::get_array()
{
  return arr;
}

template <class T>
int Vecchar<T>::get_size()
{
  return size;
}

#endif //VEC_CHAR_CLASS