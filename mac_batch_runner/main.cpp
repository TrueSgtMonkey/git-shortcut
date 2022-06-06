#include <iostream>
#include <fstream>
#include <stdlib.h>
#include "vecchar.h"

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

  Vecchar<Vecchar<char>*> vec(new Vecchar<char>);

  char c;
  while(ifs.get(c))
  {
    vec[vec.get_size()-1]->push(c);
    if(c == '\n')
    {
      vec.push(new Vecchar<char>);
    } 
  }

  for(int i = 0; i < vec.get_size(); i++)
  {
    system(vec[i]->get_array());
  }

  ifs.close();
  
  return 0;
}
