import React from 'react'

import { useForm } from "react-hook-form";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

import useAuth from "../hooks/useAuth";

const NewCar = () => {

    const [apiError, setApiError] = useState()

    const {auth} = useAuth()

    let navigate = useNavigate();

    const { register, handleSubmit, formState: { errors } } = useForm()

    const onErrors = errors => console.error(errors);
    
    const onFormSubmit  = async (data) => {
        data['owner'] = auth.id
        const response = await fetch('http://127.0.0.1:8000/cars/',{
            method:"POST",
            headers:{
                'Content-Type':'application/json',
                'Authorization':`Bearer ${auth.token}`
            },
            body:JSON.stringify(data)}        
        )

        // if the submit is successful - console
        if (response.ok){
     
            navigate("/protected", {replace:true})

        } else {
         
            let errorResponse = await response.json()
            let errArray = errorResponse.detail.map(el=>{
                return `${el.loc[1]} -${el.msg}`
            })        
            
            setApiError(errArray)
           
        }

        
 
        
    }


    
    
    return (
    <div>
        <form onSubmit={handleSubmit(onFormSubmit, onErrors)}>
            <div className="flex flex-col justify-center items-center">
                <label class="label">
                    <span class="label-text">Car brand</span>   
                </label>
                <input 
                    type="text" 
                    placeholder="brand" 
                    className="input input-bordered input-accent w-full max-w-xs m-3"
                    name="brand"
                    autoComplete="off"
                    {...register('brand',{ required: "The brand is required" })}
                />
                {errors?.brand && errors.brand.message}

                <label class="label">
                    <span class="label-text">Car model</span>   
                </label>
                <input 
                    type="text" 
                    placeholder="make" 
                    className="input input-bordered input-accent w-full max-w-xs m-3"
                    name="make"
                    autoComplete="off"
                    {...register('make',{ required: "The make is required" })}
                />
                {errors?.make && errors.make.message}

                <label class="label">
                    <span class="label-text">Production year</span>   
                </label>

                <input 
                    type="number" 
                    placeholder="year" 
                    className="input input-bordered input-accent w-full max-w-xs m-3"
                    name="year"
                    autoComplete="off"
                    {...register('year',{ required: "The year is required" })}
                />
                {errors?.year && errors.year.message}

                <label class="label">
                    <span class="label-text">Mileage in Km</span>   
                </label>
                <input 
                    type="number" 
                    placeholder="km" 
                    className="input input-bordered input-accent w-full max-w-xs m-3"
                    name="km"
                    autoComplete="off"
                    {...register('km',{ required: "The km is required" })}
                />
                {errors?.km && errors.km.message}


                <label class="label">
                    <span class="label-text">Engine displacement (cm3)</span>   
                </label>
                <input 
                    type="number" 
                    placeholder="cm3" 
                    className="input input-bordered input-accent w-full max-w-xs m-3"
                    name="cm3"
                    autoComplete="off"
                    {...register('cm3',{ required: "The cm3 is required" })}
                />
                {errors?.cm3 && errors.cm3.message}

                <label class="label">
                    <span class="label-text">Price in Euro</span>   
                </label>

                <input 
                    type="number" 
                    placeholder="price" 
                    className="input input-bordered input-accent w-full max-w-xs m-3"
                    name="price"
                    autoComplete="off"
                    {...register('price',{ required: "The price is required" })}
                />
                {errors?.price && errors.price.message}

                <button className="btn btn-outline btn-accent m-3 btn-block">Create</button>
            </div>           
       
        </form>


        {apiError && 
            <div className="alert alert-error shadow-lg">
                <div>
                    <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                    <span>{apiError}</span>
                </div>
            </div>}


    </div>
  )
}

export default NewCar