import React, {useState, useEffect} from 'react'
import styled from "styled-components";
import { Splide, SplideSlide } from "@splidejs/react-splide";
import '@splidejs/splide/dist/css/splide.min.css';
import { Link } from 'react-router-dom';

function Veggies() {

    const [veggie, setVeggies] = useState([]);

    useEffect(() => {
      const check = localStorage.getItem("veggie");
      if (check &&  check !== "undefined" ) {
        setVeggies(JSON.parse(check));
      } else {
        fetch(`/api/recipes/vegetarian`)
          .then((response) => response.json())
          .then((data) => {
            if (data) {
              localStorage.setItem("veggie", JSON.stringify(data));
              setVeggies(data);
            }
          })
          .catch((error) => console.error('Error fetching recipes:', error));
      }
    }, []);


    return (
        <>
      <Wrapper>
        <h3 className='vegetarian'>Vegetarian Picks</h3>
        <Splide
          options={{
            perPage: 4,
            arrows: false,
            pagination: false,
            drag: 'free',
            gap: '5rem',
          }}
        >
          {veggie &&
            veggie.map((recipe) => (
              <SplideSlide key={recipe.id}>
                <Card>
                  <Link to={"/recipe/"+recipe.id}>
                    <p>{recipe.title}</p>
                    <img src={recipe.image} alt={recipe.title} />
                    <Gradient />
                  </Link>
                </Card>
              </SplideSlide>
            ))}
        </Splide>
      </Wrapper>
    </>
    )
}


const Wrapper = styled.div`
  margin: 4rem 0rem;
`;

const Card = styled.div`
  min-height: 25rem;
  border-radius: 2rem;
  overflow: hidden;
  position: relative;

  img {
    border-radius: 2rem;
    position: absolute;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  p {
    position: absolute;
    z-index: 10;
    left: 50%;
    bottom: 0;
    transform: translate(-50%, 0%);
    color: white;
    width: 100%;
    text-align: center;
    font-weight: 600;
    font-size: 1rem;
    height: 40%;
    display: flex;
    justify-content: center;
    align-items: center;
  }
`;

const Gradient = styled.div`
  z-index: 3;
  position: absolute;
  width: 100%;
  height: 100%;
  background: linear-gradient(rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.5));
`;


export default Veggies