#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <queue>   
#include <vector>        
#include <string>

namespace py = pybind11;

using Element = std::pair<int,std::string>;
using MyQueue = std::queue<Element>;

std::vector<Element> queue_vector(MyQueue& q)
{
    std::vector<Element> result;
    MyQueue temp = q;

    while (!temp.empty())
    {
        result.push_back(temp.front());
        temp.pop();
    }
    return result;
}

void queue_push(MyQueue& q,int val_a,const std::string& val_b)
{
    q.push({val_a,val_b});
}

void queue_pop(MyQueue& q)
{
    if(!q.empty())
    {
        q.pop();
    }
}

void queue_clear(MyQueue& q)
{
    MyQueue empty;
    std::swap(q,empty);
}

PYBIND11_MODULE(queue_stl, m) {
    py::class_<MyQueue>(m, "Queue")
        .def(py::init<>())                           
        .def("push", &queue_push)                    
        .def("pop", &queue_pop)                      
        .def("clear", &queue_clear)
        .def("empty", &MyQueue::empty)              
        .def("__len__", &MyQueue::size)              
        .def("to_vector", &queue_vector);         
}