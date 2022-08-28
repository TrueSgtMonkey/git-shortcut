#include <iostream>
#include <fstream>
#include <stdlib.h>
#include "vecchar.h"

const char* PY_STRING = "python";
const int   PY_SIZE   = 7;

std::string getOsName();
void mac_run_python3(const Vecchar<Vecchar<char>*>&, int);

int main(int argc, const char* argv[])
{
  bool is_not_windows = getOsName().find("Windows") == -1;
  std::ifstream ifs;
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
  vec[vec.get_size()-1]->push('\0');

  for(int i = 0; i < vec.get_size(); i++)
  {
    if(is_not_windows)
    {
      mac_run_python3(vec, i);
    }
    else
    {
      system(vec[i]->get_array());
    }
  }

  ifs.close();
  
  return 0;
}

void mac_run_python3(const Vecchar<Vecchar<char>*>& vec, int i)
{
  int python_idx = vec[vec.get_size()-1]->find((char*)PY_STRING, PY_SIZE-1);
  if(python_idx != -1)
  {
    char three_check = vec[vec.get_size()-1]->get_element(PY_SIZE);
    if(three_check == '3')
    {
      system(vec[i]->get_array());
      return;
    }
    Vecchar<char> python3;
    python3.push(vec[vec.get_size()-1]->subvec(python_idx, PY_SIZE-1));
    python3.push('3');
    python3.push(vec[vec.get_size()-1]->subvec(PY_SIZE-1, vec[vec.get_size()-1]->get_size()));
    python3.push('\0');
    system(python3.get_array());
  }
}

std::string getOsName()
{
#ifdef _WIN32
  return "Windows 32-bit";
#elif _WIN64
  return "Windows 64-bit";
#elif __APPLE__ || __MACH__
  return "Mac OSX";
#elif __linux__
  return "Linux";
    #elif __FreeBSD__
    return "FreeBSD";
    #elif __unix || __unix__
    return "Unix";
    #else
    return "Other";
#endif
}
