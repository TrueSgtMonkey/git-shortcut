#include <iostream>
#include <fstream>
#include <stdlib.h>

class vecchar
{
  private:
    char* arr;
    int size;
    int capacity;
  public:
    vecchar()
    {
      size = 0;
      capacity = 1;
      arr = new char[capacity];
    }
    ~vecchar()
    {
      delete[] arr;
    }
    void push_char(char c)
    {
      this->arr[size] = c;
      size++;
      if(size >= capacity)
      {
        capacity *= 2;
        char* arr = new char[capacity];
        for(int i = 0; i < size; i++)
        {
          arr[i] = this->arr[i];
        }
        delete[] this->arr;
        this->arr = arr;
      }
    }
    char* getArr()
    {
      return this->arr;
    }

};

int main(int argc, const char* argv[])
{
  using namespace std;
  ifstream ifs;
  switch(argc)
  {
    case 1:
      ifs.open("run.bat");
      break;
    case 2:
      ifs.open(argv[1]);
      break;
  }

  vecchar vec;

  char c;
  while(ifs.get(c))
  {
    vec.push_char(c);
  }

  //cout << vec.getArr() << endl;
  system(vec.getArr());

  ifs.close();
  return 0;
}
