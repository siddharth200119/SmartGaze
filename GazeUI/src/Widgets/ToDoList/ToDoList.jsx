import React from "react";
import "./ToDoList.css"

function ToDOList(props){
    if(JSON.stringify(props.list) === JSON.stringify([])){
        return(
            <div className="todo" style={{minWidth: "100%", textAlign: "center"}}><h1 style={{color: "white"}}>No To-Do Items</h1></div>
        )
    }else{
        const options = {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: 'numeric',
            minute: 'numeric',
        };
        return(
            <div className="todo">
                <h1 style={{color: "white", textAlign: "center"}}>To Do List</h1>
                <table>
                    <thead>
                    <tr>
                        <th>Title</th>
                        <th>Due Date</th>
                        <th>Status</th>
                    </tr>
                    </thead>
                    <tbody>
                    {props.list.map((item) => (
                        <tr>
                            <th>{item.title}</th>
                            <th>{new Intl.DateTimeFormat('en-IN', options).format(new Date(item.due_date))}</th>
                            <th>{item.task_status}</th>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        )
    }
}

export default ToDOList