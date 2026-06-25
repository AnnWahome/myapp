import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import styled from "styled-components";

function Recipe() {
    let params = useParams();
    const [details, setDetails] = useState({});
    const [activeTab, setActiveTab] = useState("instructions");
  
    useEffect(() => {
      const fetchDetails = async () => {
        const data = await fetch(`/api/recipes/${params.name}`);
        const detailData = await data.json();
        setDetails(detailData);
      };

      fetchDetails();
    }, [params.name]);
  
    return (
      <DetailsWrapper>
        <div>
          <h2>{details.title}</h2>
          <img src={details.image} alt={details.title || "Recipe image"} />
        </div>
  
        <Info>
          <Button
            className={activeTab === "instructions" ? "active" : ""}
            onClick={() => setActiveTab("instructions")}
          >
            Instructions
          </Button>
          <Button
            className={activeTab === "ingredients" ? "active" : ""}
            onClick={() => setActiveTab("ingredients")}
          >
            Ingredients
          </Button>
          {activeTab === "instructions" && (
            <div>
              {details.summary && <h3>{details.summary}</h3>}
              {details.instructions && <div style={{ whiteSpace: 'pre-wrap' }}>{details.instructions}</div>}
            </div>
          )}
          {/* {activeTab === "ingredients" && (
                  <ul>
                      {details.extendedIngredients.map((ingredient) => 
                          <li key={ingredient.id}>{ingredient.original}</li>
                      )}
                  </ul>
                  )} */}
  
          {details &&
            details.extendedIngredients &&
            activeTab === "ingredients" && (
              <ul>
                {details.extendedIngredients.map((ingredient) => (
                  <li key={ingredient.id}>{ingredient.original}</li>
                ))}
              </ul>
            )}
        </Info>
      </DetailsWrapper>
    );
  }

  const DetailsWrapper = styled.div`
  margin: 10rem auto 5rem;
  width: 75%;
  max-width: 1200px;
  display: flex;
  gap: 4rem;
  align-items: flex-start;

  .active {
    background: linear-gradient(35deg, #494949, #313131);
    color: black;
  }

  h2 {
    margin-bottom: 2rem;
  }

  div:first-child {
    flex: 1;
  }

  li {
    font-size: 1rem;
    line-height: 2.5rem;
  }

  ul {
    margin-top: 2rem;
  }

  img {
    width: 100%;
    max-height: 550px;
    object-fit: cover;
    border-radius: 1rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  }

  @media (max-width: 900px) {
    flex-direction: column;
    width: 90%;
  }
`;

const Button = styled.button`
  padding: 1rem 2rem;
  color: orangered;
  background: white;
  border: 2px solid black;
  margin-right: 2rem;
  font-weight: 600;
`;

const Info = styled.div`
  flex: 3;
  margin-left: 0;
`;

export default Recipe;
